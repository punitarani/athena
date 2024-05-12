"""
Streamlit App

poetry run streamlit run app.py
"""

import streamlit as st


st.set_page_config(page_title="Athena", page_icon=":microscope:", layout="wide")
st.title("Athena Research Labs")
st.subheader("Research at The Speed of Thought")

st.write("The exponential growth of scientific literature poses significant challenges for researchers striving to stay current and ensure the originality of their work. Existing AI-assisted tools lack a fully autonomous and scientifically grounded approach to navigating the complex landscape of academic literature. Athena addresses this issue by introducing an advanced AI framework that streamlines the literature review process, facilitates idea generation, and supports hypothesis testing and claim validation.")

st.header("Technical Architecture")
st.write("Athena employs a modular architecture consisting of specialized agents that collaborate to plan, gather information, analyze data, and generate reports. The framework leverages iterative planning to break down complex research objectives, allocate tasks optimally, and adapt based on insights gained during execution. Athena's knowledge base combines an embedded bi-directional citation network, built using the OpenAlex API, with a vast collection of scientific literature. The current implementation has indexed 5,600 research papers in the neuroscience domain, amounting to over 125 million tokens in the database.")

st.header("Agents")
st.write("**Manager Agent**: The Manager serves as the central coordinator, generating comprehensive task lists based on the research plan and assigning tasks to the most suitable agents. It monitors progress, adjusts task lists, and ensures the alignment of outputs with research objectives.")
st.write("**Memory Agent**: The Memory Agent accesses the embedded citation network and scientific literature database to provide relevant information on the research topic. It retrieves papers, extracts key information, and maintains a high-level understanding of the research domain.")
st.write("**Web Agent**: The Web Agent searches the internet for the most up-to-date and relevant information, extending beyond the knowledge cutoff date of the language models. It gathers both scientific and non-scientific texts to provide a comprehensive understanding of the research topic.")
st.write("**Wiki Agent**: The Wiki Agent focuses on searching Wikipedia for reliable and well-structured scientific information. By leveraging this curated source, the Wiki Agent helps maintain accuracy and credibility throughout the research process.")
st.write("**Summarize Agent**: The Summarize Agent generates concise technical summaries of scientific papers, focusing on key data points, methodologies, results, and conclusions. It employs query generation, relevance ranking, and on-demand summarization techniques to optimize efficiency and relevance.")
st.write("**Analyze Agent**: The Analyze Agent utilizes advanced reasoning techniques, such as chain-of-thought prompting, to conduct in-depth analyses of the gathered information. It breaks down complex tasks into intermediate reasoning steps, generating well-reasoned conclusions and insights.")
st.write("**Write Agent**: The Write Agent synthesizes the information gathered and analyzed by the other agents, producing clear, coherent, and engaging reports. It tailors its writing style and structure to the specific needs of the research team, ensuring effective communication of insights.")

st.header("Implementation")
st.write("Athena manages memory and context across agents to facilitate seamless collaboration. Long-term memory stores high-level outputs, while short-term memory tracks progress within each agent. The execution pipeline demonstrates the iterative and collaborative nature of Athena, with agents working together to refine research outputs. Different types of language models are strategically employed for each agent based on their role and the required capabilities, optimizing performance and efficiency.")

st.header("Use Cases and Impact")
st.write("1. **Research Discovery**: Athena streamlines the discovery of relevant research by integrating information from embedded papers, the internet, and Wikipedia, providing researchers with a comprehensive and up-to-date knowledge base.")
st.write("2. **Idea Generation**: By encouraging creative thought while grounding ideas in scientific information, Athena facilitates the generation of novel research ideas and fosters interdisciplinary connections.")
st.write("3. **Hypothesis Testing**: Athena enables initial hypothesis testing by critically evaluating hypotheses against existing knowledge, helping researchers refine their ideas and assess feasibility.")
st.write("4. **Claim Validation**: The framework supports the validation of scientific claims by examining them for empirical support and consistency with recognized research, enhancing the credibility and reliability of research outputs.")
