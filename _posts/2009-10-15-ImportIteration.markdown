---
title: Importing an iteration using a spreadsheet
layout: page
---
When you click on the 'import iteration' in the iteration tab, you
are presented with a form where you can fill out data, and two
checkboxes. In order to use this screen:

-   Click in the 'data' field, do 'select all' (usually ctrl-a),
    end copy (usually ctrl-c)
-   Open a fresh spreadsheet and past in A1

The upper part concerns the iteration, the lower part the
stories/tasks

## Iteration

Fill out the following data in the upper part
-   **ID** if you are filling in data for an existing sprint. If
    you don't fill in the ID, Agilito will create a new iteration for
    you
-   **Name** is the sprint name. If you fill out an ID here the
    iteration identified by that ID will be renamed to this name
-   **Start**, **End** are sprint start/end dates in YYYY-MM-DD
    format. Other formats will yield funny results.

## Story/task details

In the lower part, You basically fill out your task info. Tasks
that have the same story name get rolled up into one story with
that name. The IDs are story IDs, if you want to add tasks to
existing stories you fill in their ID. If you leave this blank, a
new story will be created and the tasks will be assigned to that.

Priorities for new stories are in order stories are found in the
sheet. If the owner is filled in, it must be an existing username
for the current project (the import will complain if it isn't).
Tags are optional.

I implemented this because I couldn't keep up clicking around in
agilito during our planning sessions, so I have a dump of the
product backlog in Excel and use that during planning, and import
it. It's nowhere near perfect, but it's been useful to us. Consider
this feature beta.

## Importing

When done, select and copy the data in your spreadsheet and paste
it back into the edit box, and press Save. The checkboxes are there
so you don't inadvertently create iterations/stories.



