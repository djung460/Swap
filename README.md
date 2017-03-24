# Swap
CPSC 304 Project

## Getting Started
### Views
The views python file should only be used for rendering templates. They should not do a lot of the business logic.
Any html page should be placed inside the swap directory inside templates. Currently all the web pages are very basic
using no CSS or Javascript. If someone could take that initiative and make the site look better would be great.

### Handlers
Handlers should be the ones handling the business logic. In our case this is where we would call the majority of the
 functions found inside the models.py file.

### URLs
The file urls.py intercepts and routes http requests to the correct function. You will notice that the ones that render
a view will all go to some function inside views.py. All the other ones, once complete should go to a function that is 
inside an appropriately named handler class.

### Models
The file models.py contain a representation of the database tables. Here is where we will store the SQL queries that
we will use to operate on the database.

### Common Errors
- 4xx error make sure your urls are matching correctly
- Whenever making a post/put request be sure to add a csrf_token inside the form.
