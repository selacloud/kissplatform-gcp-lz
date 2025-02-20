import streamlit as st
from anytree import Node, RenderTree
from streamlit_markmap import markmap
import re

def extract_actual_role_name(node_string):
    # Convert the Node object to a string if it is not already a string
    node_string = str(node_string)
    
    # Regex pattern to match all occurrences of content within <span> tags
    matches = re.findall(r'<span style="color:[^;]+;">(.*?)</span>', node_string)
    
    if matches:
        # Return the last match
        return matches[-1]
    else:
        # Return None if no matches are found
        return None




# Retrieve the report and the dictionary from session state
report = st.session_state.get('report', [])
ai_company_stakeholders_keywords = st.session_state.get('ai_company_stakeholders_keywords', {})

# Display the report and the dictionary content
#st.title("Page 1 - Stakeholder Report")

if report:
    st.title("Stakeholder Report Map")
    #st.write("\n")
    
else:
    st.error("No report available. Please generate it on the main page.")
    st.stop ()
    #st.success('Thank you for generating the report.')

# Define the root node for the hierarchy
stakeholder_hierarchy = Node("Stakeholder Hierarchy")
c_suite = Node(f'<span style="color:blue;">C-Suite</span>', parent=stakeholder_hierarchy)

# Assume `ai_company_stakeholders_keywords` is retrieved from session state
ai_company_stakeholders_keywords = st.session_state.get('ai_company_stakeholders_keywords', {})
selected_domain = st.session_state.get ('selected_domain')

# Function to add a node if the role exists and has keywords, with color
def add_node_if_exists(role_name, parent_node, color="black"):
    # Check if role_name starts with "New Category:"
    if role_name.startswith("New Category"):
        # Extract the actual category name
        #st.write("debug start of new role tested", role_name)
        #actual_role_name = role_name.replace("New Category:", "").strip()
        matching_role_name = None
        for key in ai_company_stakeholders_keywords.keys():
            if key.startswith("New Category"):
                matching_role_name = key
                #st.write("debug actual new role with key:", key)
                break
        actual_role_name=matching_role_name
        #st.write('debug actual role name after match', actual_role_name)
        
        # Check if the actual role name exists in the dictionary
        if actual_role_name in ai_company_stakeholders_keywords:
            #st.write ("debug looking for keywords for new role", actual_role_name)
            keywords = ai_company_stakeholders_keywords[actual_role_name]
            if keywords:
                #st.write('debug found keywords ', keywords)
                # Create the node for the actual role name under the C-Suite node
                return Node(f'<span style="color:{color};">{actual_role_name}</span>', parent=parent_node)
            else:
                st.warning(f"No keywords found for {actual_role_name}. Stopping execution.")
                st.stop()  # This stops the execution of the Streamlit script
    else:
        # Proceed with the original logic if it's not a "New Category"
        if role_name in ai_company_stakeholders_keywords:
            keywords = ai_company_stakeholders_keywords[role_name]
            if keywords:
                # Wrapping the role name in a span tag with a color
                return Node(f'<span style="color:{color};">{role_name}</span>', parent=parent_node)
            else:
                st.warning(f"No keywords found for {role_name}. Stopping execution.")
                st.stop()  # This stops the execution of the Streamlit script

    return None


# Dynamically add nodes with specific colors based on the existence of roles

#c_suite = add_node_if_exists("C-Suite", stakeholder_hierarchy, color="blue")
csuitetest=0
for child in stakeholder_hierarchy.children:
    if 'C-Suite' in child.name:
        c_suite = child
        #st.write('debug checking for c-suite')
        csuitetest=1
        break

# If C-Suite node doesn't exist, create it
if not csuitetest:
    c_suite = Node(f'<span style="color:blue;">C-Suite</span>', parent=stakeholder_hierarchy)
    #st.write('debug c stie at the end', c_suite)
board_members = add_node_if_exists("Board Members", stakeholder_hierarchy, color="green")
investors = add_node_if_exists("Investors", stakeholder_hierarchy, color="red")

if c_suite:
    other_executives_managers = add_node_if_exists("Other Executives/Managers", c_suite, color="purple")
    if other_executives_managers:
        add_node_if_exists("Project Managers", other_executives_managers, color="orange")
        add_node_if_exists("Team Leaders", other_executives_managers, color="teal")
        add_node_if_exists("Sales & Marketing", other_executives_managers, color="pink")
        add_node_if_exists("Other Employees", other_executives_managers, color="gray")
        product_managers = add_node_if_exists("Product Managers", other_executives_managers, color="brown")
        if product_managers:
            add_node_if_exists("Programmers/Developers", product_managers, color="pink")
            add_node_if_exists("UX/UI Designers", product_managers, color="cyan")
            add_node_if_exists("Architects", product_managers, color="orange")
            add_node_if_exists("Data Scientists", product_managers, color="green")
            add_node_if_exists("Testers (QA/QC)", product_managers, color="yellow")

    domain_experts = add_node_if_exists("Domain Experts", c_suite, color="magenta")
    if domain_experts:
        #selected_domain = selected_domain  # Example of selected domain
        if selected_domain in ai_company_stakeholders_keywords["Domain Experts"]:
            Node(f'<span style="color:navy;">{selected_domain} Experts</span>', parent=domain_experts)
            for expert in ai_company_stakeholders_keywords["Domain Experts"][selected_domain]:
                Node(f'<span style="color:olive;">{expert}</span>', parent=domain_experts)

    new_category = add_node_if_exists("New Category", c_suite, color="gray")
    if new_category:
        #st.write("debug after testing new category", new_category)
        # Extract the actual role name
        actual_role_name = extract_actual_role_name(new_category)
        #st.write('debug with extracted role', actual_role_name)
        for new_stakeholder in ai_company_stakeholders_keywords[actual_role_name]:
            Node(f'<span style="color:gray;">{new_stakeholder}</span>', parent=new_category)
    
   
    
    
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