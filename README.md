TangoWithDjango
===============



This project follows the django 1.5 tutorial: Tango With Django by Leif Azzopardi and David Maxwell

See http://www.tangowithdjango.com/ for more information.

Exerpt from [Tango With Django: Overview: Design Brief](http://www.tangowithdjango.com/book/chapters/overview.html#design-brief):

> 1.4.1. Design Brief
> 
> Your client would like you to create a website called Rango that lets users browse through user-defined categories to access various web pages. In Spanish, the word rango is used to mean “a league ranked by quality” or “a position in a social hierarchy” (see https://www.vocabulary.com/dictionary/es/rango).
> 
> * For the main page of the site, they would like visitors to be able to see:
> 
>     * the 5 most viewed pages;
>     * the five most rango’ed categories; and
>     * some way for visitors to browse or search through categories.
> 
> * When a user views a category page, they would like it to display:
> 
>     * the category name, the number of visits, the number of likes;
>     * along with the list of associated pages in that category (showing the page’s title and linking to its url); and.
>     * some search functionality (via Bing’s Search API) to find other pages that can be linked to this category.
> 
> * For a particular category, the client would like the name of the category to be recorded, the number of times each category page has been visited, and how many users have clicked a “like” button (i.e. the page gets rango’ed, and voted up the social hierarchy).
> 
> * Each category should be accessible via a readable URL - for example, /rango/books-about-django/.
> 
> * Only registered users will be able to search and add pages to categories. And so, visitors to the site should be able to register for an account.
> 