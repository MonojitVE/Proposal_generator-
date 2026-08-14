import sys
import os

sys.path.append(os.path.join(os.getcwd(), 'Backend'))
from core.section_generators import generate_technology_stack, generate_workflow_diagram

def test():
    tech = generate_technology_stack("Project involves React, Node, AWS.")
    print("--- TECH STACK ---")
    print(tech)
    
    workflow = generate_workflow_diagram("Project involves React, Node, AWS.")
    print("--- WORKFLOW ---")
    print(workflow)

test()
