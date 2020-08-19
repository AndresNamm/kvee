from jinja2 import Template
from typing import Optional

def render_template(template,params) -> Optional[str]:
    tm = Template(template,variable_start_string="..{",variable_end_string="}..")
    copy_command=tm.render(params)
    return copy_command
