import streamlit as st
from anytree import Node, RenderTree
from streamlit_markmap import markmap


# Retrieve the report and the dictionary from session state
report = st.session_state.get('report', [])
if report:
    st.title("Non-AI Stakeholder Report Map")
else:
    st.error("No report available. Please generate it on the main page.")
    st.stop ()

# Define the root node for the hierarchy
stakeholder_hierarchy = Node("Non-AI Stakeholder Hierarchy")
community = Node(f'<span style="color:blue;">Community</span>', parent=stakeholder_hierarchy)   
environment = Node(f'<span style="color:green;">Environment</span>', parent=stakeholder_hierarchy)

government=Node(f'<span style="color:yellow;">Government</span>', parent=community)
directp=Node(f'<span style="color:magenta;">Directly Affected Members of Public</span>', parent=community)
directc=Node(f'<span style="color:orange;">Directly Affected Consumers</span>', parent=directp)
bene=Node(f'<span style="color:pink;">Beneficiaries</span>', parent=directp)

third=Node(f'<span style="color:brown;">3rd Parties and Providers</span>', parent=community)
nonp=Node(f'<span style="color:red;">Non-profit and Public Reviewers</span>', parent=community)

acad=Node(f'<span style="color:gray;">Academic and Research Entities</span>', parent=nonp)


# Function to generate Markdown string for Markmap
def generate_markdown_for_node(node, level=0):
    markdown = ' ' * (level * 2) + '- ' + node.name + '\n'
    for child in node.children:
        markdown += generate_markdown_for_node(child, level + 1)
    return markdown

def generate_markmap(root):
    return generate_markdown_for_node(root)

# Generate Markdown for Markmap based on the dynamic hierarchy
markdown = generate_markmap(stakeholder_hierarchy)

# Display the tree in Streamlit
#st.title("AI Company Stakeholders Hierarchy")
markmap(markdown)


