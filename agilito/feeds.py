from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from agilito.models import Project, Iteration as Sprint, UserStory, Task, TaskLog
import datetime
from django.contrib.syndication.views import feed as unauthenticated_feed

from django.http import HttpResponse
import base64
from django.contrib.auth import authenticate, login
from tagging.utils import parse_tag_input


def get_project(user, project):
    if user.is_superuser:
        return Project.objects.get(id=project)

    try:
        project = user.project_set.get(id=project)
    except Project.DoesNotExist:
        raise ObjectDoesNotExist

    return project

class Backlog(Feed):
    def get_object(self, bits):
        # In case of "/feeds/backlog/9/foo/bar/baz/", or other such clutter,
        # check that bits has only one member.
        if len(bits) != 1:
            raise ObjectDoesNotExist
        bits = [int(b) for b in bits]
        return get_project(self.request.user, bits[0])

    def title(self, project):
        return "Agilito: Backlog for %s" % project.name

    def link(self, project):
        if not project:
            raise FeedDoesNotExist
        return project.get_absolute_url()

    def description(self, project):
        return "Product backlog for %s" % project.name

    def items(self, project):
       return project.backlog()

    def categories(self, project):
        states = ['State:' + s[1] for s in UserStory.STATES.choices()]
        sizes = ['Size:' + s[1] for s in UserStory.SIZES.choices()]
        return sizes + states

    def item_link(self, story):
        return story.get_absolute_url()

    def item_pubdate(self, story):
        c = story.created
        return datetime.datetime(c.year, c.month, c.day)

    def item_categories(self, story):
        state = UserStory.STATES.label(story.state)
        size = UserStory.SIZES.label(story.size)
        cats = [state]
        if size: cats.append(size)
        return cats

class Iteration(Feed):
    def get_object(self, bits):
        if len(bits) != 2:
            raise ObjectDoesNotExist
        bits = [int(b) for b in bits]
        project = get_project(self.request.user, bits[0])
        return Sprint.objects.get(project__id = project.id, id=bits[1])

    def title(self, iteration):
        it = iteration.name
        pr = iteration.project.name
        return "Agilito: Iteration backlog for %s (%s) " % (it, pr)

    def link(self, iteration):
        if not iteration:
            raise FeedDoesNotExist
        return iteration.get_absolute_url()

    def description(self, iteration):
        it = iteration.name
        pr = iteration.project.name
        return "Iteration backlog for %s (%s) " % (it, pr)

    def items(self, iteration):
        tasks = []
        for story in UserStory.objects.filter(iteration=iteration).all():
            for task in story.task_set.all():
                tasks.append(task)

        return tasks

    def categories(self, project):
        states = ['State:' + s[1] for s in Task.STATES.choices()]
        tags = parse_tag_input(Task.tags)
        return states + tags

    def item_categories(self, task):
        state = [Task.STATES.label(task.state)]
        tags = parse_tag_input(task.tags)
        return state + tags

    def item_link(self, task):
        return task.get_absolute_url()

    def item_pubdate(self, task):
        pubdate = None
        try:
            pubdate = task.tasklog_set.latest().date
        except Task.DoesNotExist:
            pass
        except TaskLog.DoesNotExist:
            pass

        if pubdate is None:
            pubdate = task.user_story.created
            pubdate = datetime.datetime(pubdate.year, pubdate.month, pubdate.day)
        return pubdate

#############################################################################
#
def view_or_basicauth(view, request, test_func, realm = "", *args, **kwargs):
    """
    This is a helper function used by both 'logged_in_or_basicauth' and
    'has_perm_or_basicauth' that does the nitty of determining if they
    are already logged in or if they have provided proper http-authorization
    and returning the view if all goes well, otherwise responding with a 401.
    """
    if test_func(request.user):
        # Already logged in, just return the view.
        #
        return view(request, *args, **kwargs)

    # They are not logged in. See if they provided login credentials
    #
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            # NOTE: We are only support basic authentication for now.
            #
            if auth[0].lower() == "basic":
                uname, passwd = base64.b64decode(auth[1]).split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        request.user = user
                        return view(request, *args, **kwargs)

    # Either they did not provide an authorization header or
    # something in the authorization attempt failed. Send a 401
    # back to them to ask them to authenticate.
    #
    response = HttpResponse()
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response

#############################################################################
#
def logged_in_or_basicauth(realm = ""):
    """
    A simple decorator that requires a user to be logged in. If they are not
    logged in the request is examined for a 'authorization' header.

    If the header is present it is tested for basic authentication and
    the user is logged in with the provided credentials.

    If the header is not present a http 401 is sent back to the
    requestor to provide credentials.

    The purpose of this is that in several django projects I have needed
    several specific views that need to support basic authentication, yet the
    web site as a whole used django's provided authentication.

    The uses for this are for urls that are access programmatically such as
    by rss feed readers, yet the view requires a user to be logged in.  Many rss
    readers support supplying the authentication credentials via http basic
    auth (and they do NOT support a redirect to a form where they post a
    username/password.)

    Use is simple:

    @logged_in_or_basicauth()
    def your_view:
        ...

    You can provide the name of the realm to ask for authentication within.
    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request,
                                     lambda u: u.is_authenticated(),
                                     realm, *args, **kwargs)
        return wrapper
    return view_decorator

#############################################################################
#
def has_perm_or_basicauth(perm, realm = ""):
    """
    This is similar to the above decorator 'logged_in_or_basicauth'
    except that it requires the logged in user to have a specific
    permission.

    Use:

    @logged_in_or_basicauth('asforums.view_forumcollection')
    def your_view:
        ...

    """
    def view_decorator(func):
        def wrapper(request, *args, **kwargs):
            return view_or_basicauth(func, request,
                                     lambda u: u.has_perm(perm),
                                     realm, *args, **kwargs)
        return wrapper
    return view_decorator

@logged_in_or_basicauth('Agilito')
def feed(request, url, feed_dict=None):
    return unauthenticated_feed(request, url, feed_dict)
