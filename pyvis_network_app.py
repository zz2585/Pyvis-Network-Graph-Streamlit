import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read dataset (CSV)
df_interact = pd.read_csv("network.csv")

# Set header title
st.title('Network Graph of Meeting Participants')

# Define list of selection options and sort alphabetically
org_list = list(set(df_interact.orgA))
org_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_orgs = st.multiselect('Select participant(s) to visualize', org_list)

# Set info message on initial site load
if len(selected_orgs) == 0:
    st.text('Choose at least 1 participant to start')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['orgA'].isin(selected_orgs) | \
                                df_interact['orgB'].isin(selected_orgs)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'orgA', 'orgB', 'weight')

    # Initiate PyVis network object
    org_net = Network(
                       height='400px',
                       width='100%',
                       bgcolor='#222222',
                       font_color='white'
                      )

    # Take Networkx graph and translate it to a PyVis graph format
    org_net.from_nx(G)

    # Generate network with specific layout settings
    org_net.repulsion(
                        node_distance=420,
                        central_gravity=0.33,
                        spring_length=110,
                        spring_strength=0.10,
                        damping=0.95
                       )

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        org_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        org_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)

# Footer
st.markdown(
    """
    <br>
    <h6>Date: 2021/11/07</h6>
    """, unsafe_allow_html=True
    )
