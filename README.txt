The evolution of lung adenocarcinoma is accompanied by a large number of gene mutations and dysfunctions, which
makes the phenotypic state and evolutionary direction very complex. To interpret the evolution of lung adenocarcinoma,
Various methods have been developed for understanding the molecular pathogenesis and functional evolution processes.
However, most of those methods were limited due to the missing of cancerous temporal information, and the challenges
of heterogeneous characteristics. To handle these problems, in this study, a patient quasi-potential landscape method
was proposed to estimate the cancerous time of phenotypic states’ emergence during the evolutionary process,
and the oncogenetic graphs were then generated accordingly to reflect the molecular pathogenesis of lung adenocarcinoma
evolutionary process. Moreover, a feasible framework was also developed to identify functional evolution processes of lung 
adenocarcinoma, where patients were evenly re-divided into early evolutionary stage, middle evolutionary stage and late 
evolutionary stage according to cancerous time.

Description

"TCGA_LUAD_all_deg_sur_expr_info.xlsx" and "TCGA_LUAD_all_deg_sur_expr.xlsx" is the data of 560 samples' DESGs gene expression data from TCGA-LUAD, 
whose difference lies in whether it contains information such as subtypes. 
"Cancerous Time Estimation for Interpreting the Evolution of Lung Adenocarcinoma.py" is the main code to obtain the patient quasi-potential landscape of LUAD. 
The 3D figure of the landscape is drew by matlab"landscape3D.m". 
The cancerous time is calculated by "cancerous time.py".
"oncogenetic paths.rar" contains all oncogenetic paths.
"Modules_different_evolutionary_stage" contains all modules of different evolutionary stage.
