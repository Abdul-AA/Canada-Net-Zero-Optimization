# Canada-Net-Zero-Optimization

## Tools 
- Python
- Gurobi

## Context
Developing climate resilience is one of the most pressing mandates for the global community in the face
of the climate crisis. Canada, as a signatory of the Paris Agreement, has committed to achieving net-zero
greenhouse gas emissions by 2050, and to reducing its emissions by 40-45% from 2005 levels by 2030.
These ambitious targets require significant transformations in various sectors of the economy, one of
which is the electricity sector – the focus of this project.

Building on the work of the Canada Energy Regulator (CER), we sought to develop our own models
to examine the implications of Canada’s commitments for its electricity sector. This is done firstly
using a base model with a multi-objective mixed integer programming (MIP) approach, then through
an additional model centred on a goal programming (GP) approach. The base model allows us to find
an optimal solution satisfying our specified objectives and constraints, while the GP model enables us
to explore the trade-offs and compromises among the objectives when they are conflicting or infeasible.
Through the MIP formulation, we sketch out a roadmap of electricity generation and technology
investment decisions to get as near as possible to Canada’s net-zero emissions targets for the sector –
given exclusion of carbon sequestration from the model. This is done while considering mandates such
as minimizing costs and ensuring reliable energy supply. Through the GP formulation, we assess the
broader feasibility of emissions, energy generation, energy capacity, and capital cost goals over the same
time period and subject to the same reliability mandates.

Our team chose to centre our project on this problem due to its inherent complexity and the critical
role that untangling such problems plays in contemporary environmental and energy debates. Getting
Canada’s electricity sector to zero emissions by 2035 presents a multifaceted dilemma balancing environmental,
economic, and social factors. Problems like this elude straightforward understanding and greatly
benefit from methods like data modeling for conceptualization. The resulting artifacts can be powerful
tools for building shared understanding, and ideally, collective action.
The following report details the formulation and implementation of these models, their results and
their implications, potential extensions, and lessons learned regarding both the potential and the practical
limitations of linear optimization as a prescriptive analytics tool in complex and uncertain environments.

Full report available at https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/cc06ab7934bf71219d516aab8a7c509221d1cca3/Optimization.pdf
Full code notebook available at https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/e2f1826674320e892b1282befc84edae0425810d/Canada-Net-Zero%202.ipynb

View the detailed result at https://canada-net-zero.streamlit.app/
