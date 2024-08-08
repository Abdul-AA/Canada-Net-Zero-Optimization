# Canada-Net-Zero-Optimization




## Context
Developing climate resilience is one of the most pressing mandates for the global community in the face
of the climate crisis. Canada, as a signatory of the Paris Agreement, has committed to achieving net-zero
greenhouse gas emissions by 2050, and to reducing its emissions by 40-45% from 2005 levels by 2030.
These ambitious targets require significant transformations in various sectors of the economy, one of
which is the electricity sector – the focus of this project.

## The Optimization Model
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

## Results
### Optimal Energy Mix in 2025
![2025](https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/3b65bafcb3de295e2c3cc5b38d0193cf35e80909/2025.png)
### Optimal Energy Mix in 2030
![2030](https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/3b65bafcb3de295e2c3cc5b38d0193cf35e80909/2030.png)
### Optimal Energy Mix in 2035
![2035](https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/3b65bafcb3de295e2c3cc5b38d0193cf35e80909/2035.png)



Full report including the objective functions, decision variables, and constraints can be found [here](https://github.com/Abdul-AA/Canada-Net-Zero-Optimization/blob/f3542db256244222a213fa306179545a00c81f2d/Optimization.pdf)

[View the detailed result](https://canada-net-zero.streamlit.app/)
