#pip install gensim
#pip install streamlit

import warnings

import streamlit as st
import gensim.downloader as api
import numpy as np
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from io import BytesIO
import textwrap
from anytree import Node, RenderTree, AsciiStyle

# Suppress all warnings
warnings.filterwarnings("ignore")

# Global placeholder
placeholder = st.empty()

#print(gensim.__version__)

# Cache the model loading function
@st.cache_resource
def load_model():
    #return api.load('fasttext-wiki-news-subwords-300')
    return api.load ('glove-wiki-gigaword-100')

# Load the word2vec model using the cached function
with st.spinner('Application loading...'):
    model = load_model()

#st.sidebar.success("For more information, select a page above.")
#define the dictionary of keywords
ai_domains_keywords = {
    "Employee recruitment": [
        "Screening",
        "Evaluating",
        "Selecting job candidates",
        "Analyzing resumes",
        "Cover letters",
        "Application materials",
        "Hiring decisions",
        "Employee"
    ],
    "Human resources applications": [
        "Assessing employee performance",
        "Determining promotions",
        "Managing payroll",
        "Payroll"
        "Career development recommendations",
        "Tracking employee productivity",
        "Predicting employee turnover",
        "Workplace scheduling",
        "Employee"
    ],
    "Evaluating student candidates for admission": [
        "Assess applicants",
        "Academic records",
        "Extracurricular activities",
        "Personal statements",
        "Standardized test scores",
        "Admissions decisions",
        "Student"
    ],
    "Education and Training Programs": [
        "Access to educational programs",
        "Scholarships",
        "Training opportunities",
        "Assessing academic performance",
        "Aptitude tests",
        "Program eligibility",
        "Education",
        "Training"
    ],
    "Facial recognition": [
        "Identification",
        "Authentication",
        "Access control",
        "Law enforcement",
        "Personalized marketing",
        "Identity verification",
        "High-security areas"
    ],
    "Surveillance and public security and safety applications": [
        "Monitoring",
        "Public safety",
        "CCTV surveillance",
        "Crowd control",
        "Anomaly detection",
        "Predictive policing",
        "Criminal activity detection",
        "Emergency responses",
        "Urban security"
    ],
    "Autonomous weapons": [
        "Autonomous weapons systems",
        "Drones",
        "Robotic soldiers",
        "Automated military hardware",
        "Defense",
        "Warfare",
        "Target selection and engagement"
    ],
    "Healthcare Diagnosis and Treatment": [
        "Medical diagnostics",
        "Patient monitoring",
        "Treatment planning",
        "Analyzing medical images",
        "Disease progression prediction",
        "Treatment protocols",
        "Personalized medicine",
        "Telehealth",
        "Robotic surgery",
        "Medical",
        "Healthcare",
        "Medical treatment",
        "Healthcare diagnosis"
    ],
    "Autonomous Vehicles": [
        "Self-driving cars",
        "Drones",
        "Autonomous vehicles",
        "Transportation",
        "Delivery services",
        "Logistics",
        "Navigation",
        "Obstacle detection",
        "Traffic management",
        "Vehicle-to-vehicle communication"
    ],
    "Content Moderation and Censorship": [
        "Monitoring online content",
        "Moderating online content",
        "Social media posts",
        "Forums",
        "Digital platforms",
        "Harmful content detection",
        "Misinformation",
        "Hate speech"
    ],
    "Predictive Maintenance and Industrial Automation": [
        "Predicting equipment failures",
        "Optimizing maintenance schedules",
        "Automating industrial processes",
        "Manufacturing",
        "Energy management",
        "Supply chain optimization"
    ],
    "Legal Decision-Making and Judicial Applications": [
        "Predicting case outcomes",
        "Recommending legal actions",
        "Automating administrative tasks",
        "Courts",
        "Law enforcement",
        "Regulatory compliance"
        "Lawsuit",
        "Court",
        "Lawsuits"
    ],
    "Healthcare Access and Treatment Decisions": [
        "Eligibility for medical treatments",
        "Prioritizing patients for procedures",
        "Healthcare coverage decisions",
        "Medical histories",
        "Genetic information",
        "Treatment plans",
        "Access to care"
    ],
    "Employment Screening and Background Checks": [
        "Conducting background checks",
        "Evaluating employment history",
        "Suitability for job positions",
        "Analyzing criminal records",
        "Social media activity",
        "Personal data analysis"
        "Background checks"
    ],
    "Housing and Rental Applications": [
        "Screening rental applications",
        "Determining rental rates",
        "Tenant approvals",
        "Evaluating credit reports",
        "Rental histories",
        "Personal references",
        "Housing decisions"
        "Tenant",
        "Rental"
    ],
    "Generic":[
        "No information"
    ]
}

# Define the updated dictionary of keywords by role
ai_company_stakeholders_keywords = {
    "Programmers/Developers": [
        "programmers", "developers", "software architects", "security specialists"
    ],
    "Product Managers": [
        "product managers", "visionaries", "strategists", "market analysts"
    ],
    "Project Managers": [
        "project managers", "coordinators"
    ],
    "UX/UI Designers": [
        "designers", "user researchers", "usability testers"
    ],
    "Team Leaders": [
        "team leaders", "managers", "supervisors"
    ],
    "Business Analysts": [
        "business analysts", "data analysts", "strategists"
    ],
    "Architects": [
        "architects", "system architects", "infrastructure architects"
    ],
    "Data Scientists": [
        "data scientists", "researchers", "algorithm developers", "modelers"
    ],
    "Testers (QA/QC)": [
        "testers", "quality assurance specialists", "quality control specialists"
    ],
    "Investors": [
        "investors", "venture capitalists", "angel investors", "financial backers"
    ],
    "Board Members": [
        "board members", "directors", "governors"
    ],
    "C-Suite": [
        "CEO", "CTO", "CFO", "COO", "executives"
    ],
    "Other Executives/Managers": [
        "executives", "managers", "operations managers", "resource managers", "logistics managers"
    ],
    "Sales & Marketing": [
        "sales representatives", "marketers", "strategists", "campaign managers"
    ],
    "Other Employees": [
        "employees", "staff", "personnel"
    ],
    "Domain Experts": {
        "Employee recruitment": ["recruitment specialists", "HR managers", "talent acquisition experts",
                                 "screening specialists", "resume evaluators", "candidate assessors"],
        "Human resources applications": ["HR managers", "performance evaluators", "payroll specialists",
                                         "employee relations experts", "compliance officers"],
        "Evaluating student candidates for admission": ["admissions officers", "academic advisors",
                                                        "education counselors", "academic records evaluators",
                                                        "test score analysts"],
        "Education and Training Programs": ["program managers", "scholarship coordinators",
                                            "training specialists", "performance evaluators",
                                            "test analysts"],
        "Facial recognition": ["biometric experts", "security consultants", "law enforcement officers",
                               "verification specialists", "marketing analysts"],
        "Surveillance and public security and safety applications": ["public safety officers",
                                                                     "CCTV specialists",
                                                                     "crowd control specialists",
                                                                     "detection analysts",
                                                                     "policing experts"],
        "Autonomous weapons": ["military strategists", "technology experts", "drone operators",
                               "robotic designers", "military hardware specialists"],
        "Healthcare Diagnosis and Treatment": ["doctors", "nurses", "healthcare administrators",
                                               "diagnostics experts", "patient monitoring specialists",
                                               "treatment planners", "image analysts"],
        "Autonomous Vehicles": ["transportation experts", "logistics managers", "car engineers",
                                "drone operators", "navigation specialists"],
        "Content Moderation and Censorship": ["content moderators", "platform administrators",
                                              "social media analysts", "content detection experts",
                                              "misinformation analysts"],
        "Predictive Maintenance and Industrial Automation": ["maintenance engineers",
                                                             "automation specialists",
                                                             "failure analysts",
                                                             "schedule optimizers",
                                                             "process experts"],
        "Legal Decision-Making and Judicial Applications": ["legal analysts", "judicial officers",
                                                            "compliance experts",
                                                            "outcome predictors", "legal advisors"],
        "Healthcare Access and Treatment Decisions": ["healthcare administrators", "decision specialists",
                                                      "coverage analysts", "history evaluators",
                                                      "information analysts"],
        "Employment Screening and Background Checks": ["screening specialists", "history evaluators",
                                                       "suitability analysts", "record analysts",
                                                       "social media analysts"],
        "Housing and Rental Applications": ["application screeners", "rate analysts",
                                            "approval specialists", "credit evaluators",
                                            "reference checkers"],
        "Generic":[
                   "No information"
        ]                                    
    }
}

# Define the dictionary of keywords by role for non-AI company stakeholders - generic list
non_ai_company_stakeholders_keywords = {
    "Community": [
        "general public", "members"
    ],
    "Government": [
        "agencies", "public sector organizations", "regulators", "risk auditors", "regulatory agencies"
    ],
    "Environment": [
        "entities", "biodiversity", "environment"
    ],
    "Directly Affected Consumers": [
        "purchasers", "users", "customers"
    ],
    "Project Direction and Governance": [
        "boards", "committees"
    ],
    "3rd Parties and Providers": [
        "suppliers", "partners", "tech infrastructure providers", "model developers",
        "solution creators", "integrationists"
    ],
    "Wider Supplier Project Team": [
        "teams", "subcontractors", "consultants"
    ],
    "Customer Project Team": [
        "teams", "IT departments", "end-user support teams"
    ],
    "Beneficiaries": [
        "individuals", "organizations", "community organizations", "users"
    ],
    "Non-profit and Public Reviewers": [
        "reviewers", "public"
    ],
    "Academic and Research Entities": [
        "researchers"
    ],
    "Clients and Communicants of OC": [
        "clients", "communicants"
    ],
    "Future/Existing OC Employees": [
        "employees"
    ],
    "Generic": [
        "no information"
    ]
}

# Define the dictionary of domain-specific stakeholders for non-AI company stakeholders
domain_specific_non_ai_stakeholders = {
    "Employee recruitment": {
        "Community": ["job seekers", "community employment agencies"],
        "Government": ["labor departments", "employment regulatory agencies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["candidates", "applicants"],
        "Project Direction and Governance": ["hiring boards", "recruitment committees"],
        "3rd Parties and Providers": ["recruitment agencies", "HR tech providers"],
        "Wider Supplier Project Team": ["freelance recruiters", "external hiring consultants"],
        "Customer Project Team": ["company HR departments", "talent acquisition teams"],
        "Beneficiaries": ["successful candidates", "hired employees"],
        "Non-profit and Public Reviewers": ["job placement non-profits"],
        "Academic and Research Entities": ["labor market researchers"],
        "Clients and Communicants of OC": ["employers"],
        "Future/Existing OC Employees": ["new hires", "existing staff"]
    },
    "Human resources applications": {
        "Community": ["job seekers", "community employment agencies"],
        "Government": ["labor departments", "employment regulatory agencies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["employees"],
        "Project Direction and Governance": ["HR boards", "management committees"],
        "3rd Parties and Providers": ["HR software providers", "consultants"],
        "Wider Supplier Project Team": ["freelance HR consultants", "external HR advisors"],
        "Customer Project Team": ["company HR departments"],
        "Beneficiaries": ["employees", "HR managers"],
        "Non-profit and Public Reviewers": ["employment non-profits"],
        "Academic and Research Entities": ["HR researchers"],
        "Clients and Communicants of OC": ["employers"],
        "Future/Existing OC Employees": ["staff", "managers"]
    },
    "Evaluating student candidates for admission": {
        "Community": ["students", "parents"],
        "Government": ["education departments", "academic regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["applicants", "students"],
        "Project Direction and Governance": ["admissions boards", "academic committees"],
        "3rd Parties and Providers": ["education consultants", "admissions software providers"],
        "Wider Supplier Project Team": ["freelance education consultants", "external admissions advisors"],
        "Customer Project Team": ["school admissions teams"],
        "Beneficiaries": ["accepted students", "schools"],
        "Non-profit and Public Reviewers": ["education non-profits"],
        "Academic and Research Entities": ["education researchers"],
        "Clients and Communicants of OC": ["educational institutions"],
        "Future/Existing OC Employees": ["teachers", "admissions staff"]
    },
    "Education and Training Programs": {
        "Community": ["students", "trainees"],
        "Government": ["education departments", "training regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["students", "trainees"],
        "Project Direction and Governance": ["education boards", "training committees"],
        "3rd Parties and Providers": ["training providers", "education consultants"],
        "Wider Supplier Project Team": ["freelance trainers", "external education advisors"],
        "Customer Project Team": ["school training departments", "corporate training teams"],
        "Beneficiaries": ["trained individuals", "educational institutions"],
        "Non-profit and Public Reviewers": ["education non-profits"],
        "Academic and Research Entities": ["training researchers"],
        "Clients and Communicants of OC": ["educational institutions"],
        "Future/Existing OC Employees": ["teachers", "trainers"]
    },
    "Facial recognition": {
        "Community": ["privacy advocates", "general public"],
        "Government": ["security departments", "privacy regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["users of facial recognition systems"],
        "Project Direction and Governance": ["security boards", "privacy committees"],
        "3rd Parties and Providers": ["biometric tech providers", "security consultants"],
        "Wider Supplier Project Team": ["freelance security consultants", "external biometric advisors"],
        "Customer Project Team": ["company security teams"],
        "Beneficiaries": ["users", "security personnel"],
        "Non-profit and Public Reviewers": ["privacy non-profits"],
        "Academic and Research Entities": ["biometric researchers"],
        "Clients and Communicants of OC": ["security firms"],
        "Future/Existing OC Employees": ["security staff"]
    },
    "Surveillance and public security and safety applications": {
        "Community": ["residents", "general public"],
        "Government": ["public safety departments", "security regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["citizens"],
        "Project Direction and Governance": ["public safety boards", "security committees"],
        "3rd Parties and Providers": ["surveillance tech providers", "security consultants"],
        "Wider Supplier Project Team": ["freelance security consultants", "external surveillance advisors"],
        "Customer Project Team": ["public safety teams"],
        "Beneficiaries": ["citizens", "security personnel"],
        "Non-profit and Public Reviewers": ["public safety non-profits"],
        "Academic and Research Entities": ["security researchers"],
        "Clients and Communicants of OC": ["public safety organizations"],
        "Future/Existing OC Employees": ["public safety staff"]
    },
    "Autonomous weapons": {
        "Community": ["peace advocates", "general public"],
        "Government": ["defense departments", "military regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["military personnel"],
        "Project Direction and Governance": ["defense boards", "military committees"],
        "3rd Parties and Providers": ["defense tech providers", "military consultants"],
        "Wider Supplier Project Team": ["freelance defense consultants", "external military advisors"],
        "Customer Project Team": ["military teams"],
        "Beneficiaries": ["military personnel", "defense organizations"],
        "Non-profit and Public Reviewers": ["peace non-profits"],
        "Academic and Research Entities": ["military researchers"],
        "Clients and Communicants of OC": ["defense organizations"],
        "Future/Existing OC Employees": ["military staff"]
    },
    "Healthcare Diagnosis and Treatment": {
        "Community": ["patients", "general public"],
        "Government": ["health departments", "medical regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["patients"],
        "Project Direction and Governance": ["health boards", "medical committees"],
        "3rd Parties and Providers": ["medical tech providers", "health consultants"],
        "Wider Supplier Project Team": ["freelance medical consultants", "external health advisors"],
        "Customer Project Team": ["hospital teams", "clinic staff"],
        "Beneficiaries": ["patients", "medical personnel"],
        "Non-profit and Public Reviewers": ["health non-profits"],
        "Academic and Research Entities": ["medical researchers"],
        "Clients and Communicants of OC": ["health organizations"],
        "Future/Existing OC Employees": ["medical staff"]
    },
    "Autonomous Vehicles": {
        "Community": ["drivers", "general public"],
        "Government": ["transport departments", "vehicle regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["drivers", "passengers"],
        "Project Direction and Governance": ["transport boards", "vehicle committees"],
        "3rd Parties and Providers": ["vehicle tech providers", "transport consultants"],
        "Wider Supplier Project Team": ["freelance transport consultants", "external vehicle advisors"],
        "Customer Project Team": ["transport teams"],
        "Beneficiaries": ["drivers", "passengers"],
        "Non-profit and Public Reviewers": ["transport non-profits"],
        "Academic and Research Entities": ["transport researchers"],
        "Clients and Communicants of OC": ["transport organizations"],
        "Future/Existing OC Employees": ["transport staff"]
    },
    "Content Moderation and Censorship": {
        "Community": ["internet users", "general public"],
        "Government": ["media departments", "censorship regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["content creators", "platform users"],
        "Project Direction and Governance": ["media boards", "censorship committees"],
        "3rd Parties and Providers": ["content moderation tech providers", "media consultants"],
        "Wider Supplier Project Team": ["freelance media consultants", "external moderation advisors"],
        "Customer Project Team": ["platform moderation teams"],
        "Beneficiaries": ["internet users", "content creators"],
        "Non-profit and Public Reviewers": ["media non-profits"],
        "Academic and Research Entities": ["media researchers"],
        "Clients and Communicants of OC": ["media organizations"],
        "Future/Existing OC Employees": ["moderation staff"]
    },
    "Predictive Maintenance and Industrial Automation": {
        "Community": ["workers", "general public"],
        "Government": ["industry departments", "industrial regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["factory workers"],
        "Project Direction and Governance": ["industry boards", "automation committees"],
        "3rd Parties and Providers": ["industrial automation tech providers", "maintenance consultants"],
        "Wider Supplier Project Team": ["freelance industrial consultants", "external maintenance advisors"],
        "Customer Project Team": ["factory maintenance teams"],
        "Beneficiaries": ["workers", "industrial personnel"],
        "Non-profit and Public Reviewers": ["industry non-profits"],
        "Academic and Research Entities": ["industrial researchers"],
        "Clients and Communicants of OC": ["industrial organizations"],
        "Future/Existing OC Employees": ["industrial staff"]
    },
    "Legal Decision-Making and Judicial Applications": {
        "Community": ["citizens", "general public"],
        "Government": ["justice departments", "legal regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["litigants"],
        "Project Direction and Governance": ["legal boards", "judicial committees"],
        "3rd Parties and Providers": ["legal tech providers", "judicial consultants"],
        "Wider Supplier Project Team": ["freelance legal consultants", "external judicial advisors"],
        "Customer Project Team": ["court teams"],
        "Beneficiaries": ["litigants", "legal personnel"],
        "Non-profit and Public Reviewers": ["legal non-profits"],
        "Academic and Research Entities": ["legal researchers"],
        "Clients and Communicants of OC": ["legal organizations"],
        "Future/Existing OC Employees": ["legal staff"]
    },
    "Healthcare Access and Treatment Decisions": {
        "Community": ["patients", "general public"],
        "Government": ["health departments", "medical regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["patients"],
        "Project Direction and Governance": ["health boards", "medical committees"],
        "3rd Parties and Providers": ["medical access tech providers", "health consultants"],
        "Wider Supplier Project Team": ["freelance health consultants", "external medical advisors"],
        "Customer Project Team": ["hospital access teams", "clinic staff"],
        "Beneficiaries": ["patients", "medical personnel"],
        "Non-profit and Public Reviewers": ["health non-profits"],
        "Academic and Research Entities": ["medical researchers"],
        "Clients and Communicants of OC": ["health organizations"],
        "Future/Existing OC Employees": ["medical staff"]
    },
    "Employment Screening and Background Checks": {
        "Community": ["job seekers", "general public"],
        "Government": ["labor departments", "employment regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["candidates", "employees"],
        "Project Direction and Governance": ["hiring boards", "screening committees"],
        "3rd Parties and Providers": ["screening tech providers", "HR consultants"],
        "Wider Supplier Project Team": ["freelance screening consultants", "external hiring advisors"],
        "Customer Project Team": ["company HR departments", "talent acquisition teams"],
        "Beneficiaries": ["candidates", "employees"],
        "Non-profit and Public Reviewers": ["employment non-profits"],
        "Academic and Research Entities": ["employment researchers"],
        "Clients and Communicants of OC": ["employers"],
        "Future/Existing OC Employees": ["new hires", "existing staff"]
    },
    "Housing and Rental Applications": {
        "Community": ["tenants", "general public"],
        "Government": ["housing departments", "rental regulatory bodies"],
        "Environment": ["none"],
        "Directly Affected Consumers": ["tenants", "applicants"],
        "Project Direction and Governance": ["housing boards", "rental committees"],
        "3rd Parties and Providers": ["rental tech providers", "housing consultants"],
        "Wider Supplier Project Team": ["freelance housing consultants", "external rental advisors"],
        "Customer Project Team": ["housing management teams"],
        "Beneficiaries": ["tenants", "applicants"],
        "Non-profit and Public Reviewers": ["housing non-profits"],
        "Academic and Research Entities": ["housing researchers"],
        "Clients and Communicants of OC": ["landlords"],
        "Future/Existing OC Employees": ["property managers"]
    },
    "Generic": {
        "Community": ["NA"],
        "Government": ["NA"],
        "Environment": ["NA"],
        "Directly Affected Consumers": ["NA"],
        "Project Direction and Governance": ["NA"],
        "3rd Parties and Providers": ["NA"],
        "Wider Supplier Project Team": ["NA"],
        "Customer Project Team": ["NA"],
        "Beneficiaries": ["NA"],
        "Non-profit and Public Reviewers": ["NA"],
        "Academic and Research Entities": ["NA"],
        "Clients and Communicants of OC": ["NA"],
        "Future/Existing OC Employees": ["NA"]
    }
}

# Initialize session state variables
if 'description_input' not in st.session_state:
    st.session_state.description_input = st.empty()

if 'domain_selection' not in st.session_state:
    st.session_state.domain_selection = st.empty()

if 'stakeholder_report' not in st.session_state:
    st.session_state.stakeholder_report = st.empty()

if 'final_report' not in st.session_state:
    st.session_state.final_report = st.empty()

if 'show_complete_list' not in st.session_state:
    st.session_state.show_complete_list = False

if 'domain_ranks' not in st.session_state:
    st.session_state.domain_ranks = None

if 'selected_domain' not in st.session_state:
    st.session_state.selected_domain = None

if 'report' not in st.session_state:
    st.session_state.report = []

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'description_input'



# Define the real AI domain selection functions
def get_mean_vector(model, words):
    # Remove out-of-vocabulary words
    words = [word for word in words if word in model.key_to_index]
    if len(words) >= 1:
        return np.mean(model[words], axis=0)
    else:
        return np.zeros(model.vector_size)

def find_best_matching_domain(user_description, model, ai_domains_keywords):
    user_vector = get_mean_vector(model, user_description.lower().split())
    similarities = {}

    for domain, keywords in ai_domains_keywords.items():
        keyword_vectors = [model.get_vector(keyword.lower()) for keyword in keywords if keyword.lower() in model]
        if keyword_vectors:
            domain_vector = np.mean(keyword_vectors, axis=0)
            similarity = np.dot(user_vector, domain_vector) / (np.linalg.norm(user_vector) * np.linalg.norm(domain_vector))
            similarities[domain] = similarity

    return similarities

def find_all_ai_domains_with_ranks(user_description):
    similarities = find_best_matching_domain(user_description, model, ai_domains_keywords)
    return similarities


# Define the function to generate PDF using reportlab
def generate_pdf(report):
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    line_count=0
    
    text_object = c.beginText(40, height - 40)
    text_object.setFont("Helvetica", 12)

    # Define the maximum number of lines per page
    max_lines_per_page = 49  # Adjust based on font size and margins
    #st.write("max lines per page", max_lines_per_page)
    line_count = 0
    
    # Ensure text wraps properly
    for line in report:
        # Split the line on double newlines
        parts = line.split('\n\n')
        for part in parts:
            wrapped_lines = textwrap.wrap(part, width=80)  # Adjust the width as needed
            for wrapped_line in wrapped_lines:
                text_object.textLine(wrapped_line)
                line_count += 1
            # Check if we need to start a new page
                if line_count >= max_lines_per_page:
                    c.drawText(text_object)
                    c.showPage()
                    text_object = c.beginText(40, height - 40)
                    text_object.setFont("Helvetica", 12)
                    line_count = 0
            
            # Add an empty line to simulate the \n\n
            text_object.textLine("")
            line_count += 1
            
            if line_count >= max_lines_per_page:
                c.drawText(text_object)
                c.showPage()
                text_object = c.beginText(40, height - 40)
                text_object.setFont("Helvetica", 12)
                line_count = 0
    
    c.drawText(text_object)  # Finalize the text object by drawing it onto the canvas
    c.showPage()  # Finish the current page
    c.save()  # Finalize the PDF and save it to the buffer
    
    pdf_buffer.seek(0)  # Move the buffer's position to the start
    return pdf_buffer

def find_matching_domains(user_description):
    st.write("Finding matching domains...")  # Debug statement
    st.session_state.domain_ranks = find_all_ai_domains_with_ranks(user_description)
    st.session_state.show_complete_list = False
    st.session_state.current_view = 'domain_selection'
    display_view()

# Define view display functions
def display_description_input():
    st.session_state.description_input.empty()
    global placeholder
    placeholder.empty()
    with placeholder.container():
        st.title('Find Your AI Project Stakeholders by Industry Domain')
        st.write("Enter a description of the user's requirements, and this tool will suggest stakeholders according to the best matching industry domains.")
        user_description = st.text_area("User Description")

        
        
        if st.button("Find Matching Domains"):
            find_matching_domains(user_description)
            


def display_domain_selection():
    with st.spinner('Application loading...'):
        #st.write('debug display domain selection')
        time.sleep(2)
    global placeholder
    placeholder.empty()
    
    with placeholder.container():
        st.title('Find Your AI Project Stakeholders by Industry Domain')  # Re-add the title
        #st.write("Debug: Entering display_domain_selection")  # Debug statement
        if st.session_state.domain_ranks:
            sorted_domains = sorted(st.session_state.domain_ranks.items(), key=lambda item: item[1], reverse=True)
            st.write("The top 3 Industry Domains that match your description, ranked by relevance, are:")
            top_domains = sorted_domains[:3]
            for idx, (domain, _) in enumerate(top_domains, start=1):
                st.write(f"{idx}. {domain}")

            user_choice = st.radio(
                "Do you want to select from this list or see the complete list of domains?",
                ('Select from this list', 'See the complete list of domains'),
                key='domain_selection_radio_1'
            )
            #st.write(f"Debug: user_choice = {user_choice}")  # Debug statement

            if user_choice == 'Select from this list':
                selected_index = st.number_input("Please enter the number of the offered domain that best matches your AI project:", min_value=1, max_value=len(top_domains), step=1, key='domain_selection_number_input_1')
                st.session_state.selected_domain = top_domains[selected_index - 1][0]
                #st.write(f"Debug: selected_domain = {st.session_state.selected_domain}")  # Debug statement
            elif user_choice == 'See the complete list of domains':
                st.session_state.show_complete_list = True
                #st.write("Debug: user_choice = See the complete list of domains")  # Debug statement

            if st.button("Confirm Your Selection"):
                #st.write("Debug: Confirm Selection button clicked")  # Debug statement
                time.sleep(2)  # Adding a delay of 2 seconds
                if user_choice == 'See the complete list of domains':
                    st.session_state.current_view = 'complete_domain_list'
                else:
                    st.session_state.current_view = 'stakeholder_report'
                placeholder.empty()  # Clear the screen
                display_view()
        else:
            st.write("Debug: No domain ranks found")  # Debug statement

def display_complete_domain_list():
    st.session_state.domain_selection.empty()
    global placeholder
    placeholder.empty()

    with placeholder.container():
        st.title('Find Your AI Project Stakeholders by Industry Domain')
        #st.write("Debug: Entering display_complete_domain_list")

        all_domains = list(st.session_state.domain_ranks.keys())
        for idx, domain in enumerate(all_domains, start=1):
            st.write(f"{idx}. {domain}")

        
        all_domains = list(st.session_state.domain_ranks.keys())

        # Use slider instead of number_input
        selected_index = st.slider("Please select the domain that best matches your AI project:", 
                           min_value=1, max_value=len(all_domains), step=1) - 1

        st.session_state.selected_domain = all_domains[selected_index]
        #st.write(f"Debug Selected domain: {st.session_state.selected_domain}")
                # Make sure the key is unique for this widget
        missing_domain_choice = st.radio("Do you think your preferred domain is missing?",
                                         ('no', 'yes'), key='complete_domain_list_radio_2')
        
        if missing_domain_choice == 'yes':
            st.session_state.selected_domain = st.text_input("Please enter the name of the preferred domain that you think is missing:",
                                                             key='complete_domain_list_text_input_2')
            #st.write(f"Debug: entered missing domain = {st.session_state.selected_domain}")
            st.session_state.selected_domain = 'Generic'

        if st.button("Confirm Selection"):
            #st.write("Debug: Confirm Selection button clicked in display_complete_domain_list")
            st.session_state.current_view = 'stakeholder_report'
            display_view()



def create_stakeholder_report(selected_domain):
    report = []  # Initialize an empty list to accumulate the report lines
    
    # Add the introductory text and explanation
    combined_text = "Here is your stakeholder report for" + " " + selected_domain
    report.append(combined_text)
    
    # New text to be added with line breaks after each sentence
    importance_text = (
        "Why this report is important:\n"
        "The report is crucial for ensuring comprehensive stakeholder consideration, ethical AI development, "
        "risk mitigation, and regulatory compliance.\n\n"
        "What it shows:\n"
        "It demonstrates methods for stakeholder mapping, impact analysis, engagement strategies, "
        "and practical application through a case study.\n\n"
        "How to use it:\n"
        "The report provides a step-by-step guide for identifying and analyzing stakeholders, "
        "developing engagement strategies, addressing ethical concerns, and ensuring ongoing monitoring and compliance in AI projects.\n"
    )
    report.append(importance_text)
    report.append("")  # Add two empty lines for separation
    report.append("")

    # Add AI company stakeholders to the report
    report.append("**Your AI Company Stakeholders:**")
    for role, keywords in ai_company_stakeholders_keywords.items():
        if role == "Domain Experts":
            report.append(f"{role}: {', '.join(ai_company_stakeholders_keywords[role][selected_domain])}")
        else:
            report.append(f"{role}: {', '.join(keywords)}")
    
    # Add non-AI company stakeholders to the report
    report.append("")  # Empty line for separation
    report.append("**Your Non-AI Company Stakeholders:**")
    for category, stakeholders in domain_specific_non_ai_stakeholders[selected_domain].items():
        report.append(f"{category}: {', '.join(stakeholders)}")
    
    # Display the report so far
    for line in report:
        st.write(line)
    
    # Ask the user if any stakeholder category is missing
    #st.write("Debug: first radio")
    category_missing = st.radio("Do you think a stakeholder category is still missing?", ('no', 'yes'), key='stakeholder_category_missing_radio_1')
    

    if category_missing == 'yes':
        stakeholder_type = st.radio("Is the missing category for (a) AI company stakeholders or (b) non-AI company stakeholders?", ('a', 'b'), key='stakeholder_category_type_radio_2')
        new_category = st.text_input("Please enter the name of the missing stakeholder category:", key='stakeholder_category_name_text_input_2')
        new_stakeholders = st.text_area(f"Please enter the stakeholders for {new_category} (comma-separated):", key='stakeholder_category_stakeholders_text_area_2').split(',')
        if stakeholder_type == 'a':
            new_category_text = f"New Category: {new_category}"
            ai_company_stakeholders_keywords[new_category_text] = new_stakeholders
            #st.write('debug new stake', new_category_text, ai_company_stakeholders_keywords[new_category_text])
            
        elif stakeholder_type == 'b':
            domain_specific_non_ai_stakeholders[selected_domain][new_category] = new_stakeholders
        new_category_text = f"**New Category: {new_category}**"
        #st.write("debug", new_category_text)
        stakeholders_text = f"**Stakeholders: {', '.join(new_stakeholders)}**"
        report.append(new_category_text)
        report.append(stakeholders_text)
        st.write(new_category_text)
        st.write(stakeholders_text)
    
    # Ask the user if any specific stakeholder within a category is missing
    #st.write("Debug: second radio")
    stakeholder_missing = st.radio("Do you think a specific stakeholder within a category is missing?", ('no', 'yes'), key='specific_stakeholder_missing_radio_2')
    

    if stakeholder_missing == 'yes':
        stakeholder_type = st.radio("Is the missing stakeholder for (a) AI company stakeholders or (b) non-AI company stakeholders?", ('a', 'b'), key='specific_stakeholder_type_radio_2')
        category = st.text_input("Please enter the category where the stakeholder is missing:", key='specific_stakeholder_category_text_input_2')
        new_stakeholder = st.text_input("Please enter the missing stakeholder:", key='specific_stakeholder_name_text_input_2')
        if stakeholder_type == 'a':
            if category in ai_company_stakeholders_keywords:
                ai_company_stakeholders_keywords[category].append(new_stakeholder)
            else:
                category_not_found_text = f"Category {category} not found in AI company stakeholders."
                report.append(category_not_found_text)
                st.write(category_not_found_text)
        elif stakeholder_type == 'b':
            if category in domain_specific_non_ai_stakeholders[selected_domain]:
                domain_specific_non_ai_stakeholders[selected_domain][category].append(new_stakeholder)
            else:
                category_not_found_text = f"Category {category} not found in non-AI company stakeholders."
                report.append(category_not_found_text)
                st.write(category_not_found_text)
        
        missing_stakeholder_text = f"**Category: {category}**"
        stakeholder_text = f"**Missing Stakeholder: {new_stakeholder}**"
        report.append(missing_stakeholder_text)
        report.append(stakeholder_text)
        st.write(missing_stakeholder_text)
        st.write(stakeholder_text)
    
    

    st.session_state['ai_company_stakeholders_keywords'] = ai_company_stakeholders_keywords
    # The text broken down into individual lines to ensure line breaks in the PDF
    text_to_append = [
    "",    
    "Why this report is important:",
    "1. Comprehensive stakeholder identification: The report emphasizes the importance of considering a wide range of stakeholders affected by AI projects, from direct users to indirect beneficiaries and even the environment.",
    "2. Ethical considerations: It highlights the need to consider ethical implications and potential biases in AI systems, which is crucial for responsible AI development.",
    "3. Risk mitigation: By identifying and analyzing stakeholders, companies can anticipate potential issues and mitigate risks associated with AI implementation.",
    "4. Compliance: The report helps ensure that AI projects comply with relevant regulations and ethical guidelines.",
    "",
    "What it shows:",
    "1. Stakeholder mapping: The report provides various methods for visualizing and categorizing stakeholders, such as \"donut\" diagrams, network graphs, and matrices.",
    "2. Impact analysis: It demonstrates how to assess the potential impacts of AI systems on different stakeholder groups.",
    "3. Engagement strategies: The report outlines approaches for engaging with different types of stakeholders based on their influence and interest levels.",
    "4. Case study application: The Acme Solutions example shows how these principles can be applied to a specific AI use case (job applicant screening).",
    "",
    "How to use it:",
    "1. Identify stakeholders: Use the provided frameworks and examples to create a comprehensive list of stakeholders for your specific AI project.",
    "2. Analyze stakeholders: Apply the various matrix tools (e.g., Power-Interest Grid, Influence-Interest Matrix) to categorize and prioritize stakeholders.",
    "3. Develop engagement strategies: Based on the stakeholder analysis, create tailored communication and engagement plans for each stakeholder group.",
    "4. Consider ethical implications: Use the report's guidance to assess potential biases and ethical concerns in your AI system.",
    "5. Implement continuous monitoring: Regularly review and update your stakeholder analysis throughout the project lifecycle.",
    "6. Ensure diverse perspectives: Use the report's recommendations to include a wide range of viewpoints in your AI development process.",
    "7. Address legal and regulatory requirements: Use the report's insights to ensure your AI project complies with relevant laws and regulations.",
    "",
    "By utilizing this type of stakeholder report, companies can develop more responsible, ethical, and effective AI systems that consider the needs and concerns of all affected parties."
    ]

    # Appending each line separately to the report list
    report.extend(text_to_append)
    
    st.session_state['report'] = report
    st.session_state['selected_domain']=selected_domain
      
    return report  # Return the complete report as a list with the keywords




def display_stakeholder_report():
    st.session_state.stakeholder_report.empty()
   
    global placeholder
    placeholder.empty()
    with placeholder.container():
        st.title('Find Your AI Project Stakeholders by Industry Domain')  # Re-add the title
        st.header(f"Selected Domain: {st.session_state.selected_domain}")
        (st.session_state.report) = create_stakeholder_report(st.session_state.selected_domain)

        #st.write("Debug: st.session_state.report =", st.session_state.report)
        #st.write("Debug: st.session_state.report =")

    
        st.markdown("""
            <style>
            .stButton {
                position: fixed;
                bottom: 20px;
                right: 20px;
            }
            </style>
        """, unsafe_allow_html=True)

        if st.button("Finalize Report"):
            placeholder.empty()
            with placeholder.container():
                #st.write("Debug: st.session_state.report =", st.session_state.report)
                #st.write("Debug: st.session_state.report =")

                st.title('Find Your AI Project Stakeholders by Industry Domain')  # Re-add the title
                st.session_state.current_view = 'final_report'
                
                display_view()
        



def display_final_report():
    st.session_state.final_report.empty()
    global placeholder
    placeholder.empty()
    st.session_state.current_view = 'final_report'
    #st.write("Debug: st.session_state.report =", st.session_state.report)

        
    with placeholder.container():
        st.title('Find Your AI Project Stakeholders by Industry Domain')  # Re-add the title

        #st.write("Debug: st.session_state.report =", st.session_state.report)
        #st.write("Debug: st.session_state.report =")

        st.header("Final Report - Scroll Down to Download")
        #st.write(f"Your report for stakeholders for {st.session_state.selected_domain}")
        for line in st.session_state.report:
            st.write(line)

        #st.write(f"debug printing out report again")
        #for line in st.session_state.report:
          #  st.write(line)

        pdf_buffer = generate_pdf(st.session_state.report)
        
        st.download_button(label="Download PDF", data=pdf_buffer, file_name="report.pdf", mime='application/pdf')
        st.write(f":violet[Hit Refresh in the Web Browser to Do Again]")    


def display_view():
    global placeholder
    
    #st.write(f"Debug: current_view = {st.session_state.current_view}")  # Debug statement
    st.write(f"")
    if st.session_state.current_view == 'description_input':
        #placeholder.empty()
        display_description_input()
    elif st.session_state.current_view == 'domain_selection':
        #placeholder.empty()
        display_domain_selection()
    elif st.session_state.current_view == 'complete_domain_list':
        #placeholder.empty()
        display_complete_domain_list()
    elif st.session_state.current_view == 'stakeholder_report':
        placeholder.empty()
        display_stakeholder_report()
    elif st.session_state.current_view == 'final_report':
        placeholder.empty()
        display_final_report()

# Start the app by displaying the current view
#if __name__ == "__main__":
 #   placeholder = st.empty()
display_view()
