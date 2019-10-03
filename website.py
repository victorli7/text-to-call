import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def render(page, variables):
    navbar_title = 'Leave a message'

    template_values = {
        'page': page,
        'child': variables,
    }
    template = JINJA_ENVIRONMENT.get_template(page)
    return template.render(template_values)
