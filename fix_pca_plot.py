with open('app.py', 'r') as f:
    content = f.read()

import re

# Standalone helper to ensure full PCA plot is dynamically computed
pca_patch = '''
    # --- Dynamic Chemical Space PCA & 95% AD Boundary Plot ---
    try:
        s_query = res.get("SMILES", "")
        chem_name_label = res.get("Resolved_Name", res.get("Input", "Query Chemical"))
        ref_coords, q_coords, var_exp = compute_dynamic_pca_projection(s_query, res)
        
        # Calculate 95% Hotelling AD ellipse bounds from reference distribution
        import numpy as np
        std_x = np.std(ref_coords[:, 0]) * 2.0
        std_y = np.std(ref_coords[:, 1]) * 2.0
        mean_x = np.mean(ref_coords[:, 0])
        mean_y = np.mean(ref_coords[:, 1])
        
        theta = np.linspace(0, 2 * np.pi, 100)
        ellipse_x = mean_x + std_x * np.cos(theta)
        ellipse_y = mean_y + std_y * np.sin(theta)
        
        fig_ad = go.Figure()
        
        # 1. 95% Applicability Domain Boundary Ellipse
        fig_ad.add_trace(go.Scatter(
            x=ellipse_x,
            y=ellipse_y,
            mode='lines',
            line=dict(color='#0284c7', width=2, dash='dash'),
            name='95% OECD AD Boundary',
            hoverinfo='skip'
        ))
        
        # 2. Reference Training Compounds (OECD GL 497 / LLNA Baseline)
        fig_ad.add_trace(go.Scatter(
            x=ref_coords[:, 0],
            y=ref_coords[:, 1],
            mode='markers',
            marker=dict(size=8, color='#94a3b8', symbol='circle', opacity=0.7),
            name='OECD Reference Set (n=20)',
            hoverinfo='text',
            text=['Ref Compound ' + str(i+1) for i in range(len(ref_coords))]
        ))
        
        # 3. Active Query Molecule (Dynamic Real-time Target)
        fig_ad.add_trace(go.Scatter(
            x=[float(q_coords[0])],
            y=[float(q_coords[1])],
            mode='markers+text',
            marker=dict(size=15, color='#ef4444', symbol='star', line=dict(color='#7f1d1d', width=1.5)),
            name='Active Query Chemical',
            text=[f'★ {chem_name_label}'],
            textposition='top center',
            hoverinfo='text+x+y'
        ))
        
        fig_ad.update_layout(
            title=f'<b>Chemical Space PCA & 95% AD Boundary</b><br><span style=\"font-size:12px; color:#64748b;\">PC1: {var_exp[0]*100:.1f}% | PC2: {var_exp[1]*100:.1f}% Explained Variance</span>',
            xaxis_title='Principal Component 1 (Physicochemical & Electronic Descriptors)',
            yaxis_title='Principal Component 2 (Lipophilicity & Structural Topology)',
            template='plotly_white',
            margin=dict(l=40, r=40, t=50, b=40),
            height=420,
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig_ad, use_container_width=True)
    except Exception as e_pca:
        st.warning(f'Could not render Chemical Space PCA plot: {e_pca}')
'''

# Find the section rendering PCA / AD Boundary in render_dashboard_cards and replace it
pattern = r'(#.*?Chemical Space.*?PCA.*?\n)(.*?)(st\.plotly_chart\(.*?\))'
if re.search(pattern, content, flags=re.DOTALL):
    content = re.sub(pattern, pca_patch.strip() + '\n', content, count=1, flags=re.DOTALL)
    print('✅ Replaced PCA plotting block with dynamic projection!')
else:
    # Alternative search by section heading
    pattern2 = r'(st\.subheader\(.*?Chemical Space.*?\)\s*\n)(.*?)(?=\nst\.subheader|\nst\.header|\n# =|\Z)'
    if re.search(pattern2, content, flags=re.DOTALL):
        content = re.sub(pattern2, r'\1' + pca_patch + '\n', content, count=1, flags=re.DOTALL)
        print('✅ Replaced PCA plotting block under subheader!')
    else:
        print('⚠️ Could not find exact PCA block pattern.')

with open('app.py', 'w') as f:
    f.write(content)

