import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ==============================================================================
# CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Dashboard Caixinha | Viagem",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CSS EXECUTIVO PERSONALIZADO (REMOÇÃO DO DEPLOY, CABEÇALHO E VISUAL ELEGANTE)
# ==============================================================================
st.markdown("""
<style>
    header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stToolbar"] {
        display: none !important;
        visibility: hidden !important;
    }
    #MainMenu {
        visibility: hidden !important;
        display: none !important;
    }
    footer {
        visibility: hidden !important;
        display: none !important;
    }
    
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 98% !important;
    }

    .kpi-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 15px -1px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .kpi-container:hover {
        transform: translateY(-2px);
        border-color: #3B82F6;
    }
    .kpi-title {
        font-size: 0.72rem;
        font-weight: 700;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
    }
    .kpi-value {
        font-size: 1.6rem;
        font-weight: 900;
        color: #F8FAFC;
        letter-spacing: -0.02em;
    }
    .kpi-badge-green {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 6px;
    }
    .kpi-badge-blue {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 6px;
    }
    .kpi-badge-amber {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.3);
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 6px;
    }
    .kpi-badge-white {
        display: inline-flex;
        align-items: center;
        padding: 2px 8px;
        background: rgba(248, 250, 252, 0.15);
        color: #F8FAFC;
        border: 1px solid rgba(248, 250, 252, 0.3);
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 6px;
    }
    
    .rate-pill {
        display: inline-block;
        padding: 4px 12px;
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 20px;
        font-size: 0.78rem;
        color: #CBD5E1;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .rate-pill strong {
        color: #F8FAFC;
    }
    
    /* =========================================
       AJUSTES PARA CELULAR E TABLET (RESPONSIVO)
       ========================================= */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
        .kpi-container {
            padding: 12px 10px;
        }
        .kpi-title {
            font-size: 0.65rem;
        }
        .kpi-value {
            font-size: 1.3rem;
        }
        h1 {
            font-size: 1.4rem !important;
        }
        .rate-pill {
            font-size: 0.7rem;
            padding: 3px 8px;
            margin-bottom: 4px;
        }
    }
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = 'Caixinha.xlsx'

@st.cache_data(ttl=2)
def load_data():
    if not os.path.exists(EXCEL_FILE):
        return None, None, None, None, None, None
        
    df = pd.read_excel(EXCEL_FILE, sheet_name='Caixinha', header=None)
    
    try:
        meta_total = float(df.iloc[1, 1])
        total_juros = float(df.iloc[2, 4])
    except:
        meta_total = 12000.0
        total_juros = 0.0

    try:
        df_meta = pd.read_excel(EXCEL_FILE, sheet_name='Meta', header=None)
        meta_indiv = float(df_meta.iloc[0, 3])
    except:
        meta_indiv = 4000.0
    
    try:
        total_idx = df[df[0] == 'TOTAL'].index[0]
    except:
        total_idx = len(df)
        
    data_df = df.iloc[6:total_idx]
    
    pessoas_data = []
    timeline_data = []
    
    col_nome = "Participante"
    for val_col, date_col in [(1, 2), (3, 4), (5, 6), (7, 8)]:
        nome = str(df.iloc[5, val_col]).strip()
        if nome == 'nan' or nome == '':
            continue
            
        vals = pd.to_numeric(data_df[val_col], errors='coerce').fillna(0)
        depositos = vals[vals > 0].sum()
        retiradas = vals[vals < 0].sum()
        liquido = depositos + retiradas
        
        pessoas_data.append({
            col_nome: nome,
            'Total_Depositos': float(depositos),
            'Total_Retiradas': float(retiradas),
            'Total_Liquido': float(liquido)
        })
        
        for _, row in data_df.iterrows():
            v = row[val_col]
            d = row[date_col]
            if pd.notna(v) and v != 0 and pd.notna(d):
                timeline_data.append({
                    'Nome': nome,
                    'Data': pd.to_datetime(d),
                    'Valor': float(v),
                    'Tipo': 'Depósito' if float(v) > 0 else 'Retirada'
                })
                
    pessoas_only = pd.DataFrame(pessoas_data)
    
    df_timeline = pd.DataFrame(timeline_data)
    if not df_timeline.empty:
        df_timeline = df_timeline.sort_values('Data')
        df_timeline['Mes_Ano'] = df_timeline['Data'].dt.strftime('%Y-%m')
        
    return pessoas_only, total_juros, meta_total, meta_indiv, df_timeline, col_nome

pessoas_only, total_juros, meta_total, meta_indiv, df_timeline, col_nome = load_data()

if pessoas_only is None:
    st.error(f"Arquivo {EXCEL_FILE} não encontrado!")
    st.stop()

total_depositos = pessoas_only['Total_Depositos'].sum()
total_retiradas = pessoas_only['Total_Retiradas'].sum()
total_arrecadado = pessoas_only['Total_Liquido'].sum() + total_juros
falta_meta = max(0, meta_total - total_arrecadado)
pct_meta = (total_arrecadado / meta_total) * 100 if meta_total > 0 else 0

# ==============================================================================
# CABEÇALHO EXECUTIVO
# ==============================================================================
col_head1, col_head2, col_head3 = st.columns([5, 3, 1])

with col_head1:
    st.markdown("""
    <div style="padding-bottom: 4px;">
        <h1 style="font-size: 1.9rem; font-weight: 900; color: #F8FAFC; margin: 0; padding: 0; letter-spacing: -0.02em;">
            DASHBOARD CAIXINHA | VIAGEM
        </h1>
        <p style="font-size: 0.88rem; color: #94A3B8; margin-top: 3px;">
            Acompanhamento de Arrecadação, Rendimentos e Meta
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_head2:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 6px;">
        <span class="rate-pill">Meta Viagem: <strong>R$ {meta_total:,.2f}</strong></span>
        <span class="rate-pill">Meta Individual: <strong>R$ {meta_indiv:,.2f}</strong></span>
    </div>
    """, unsafe_allow_html=True)

with col_head3:
    st.markdown("<div style='padding-top: 12px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Atualizar", use_container_width=True, type="primary"):
        load_data.clear()
        st.rerun()

# ==============================================================================
# BARRA DE KPIS EXECUTIVOS
# ==============================================================================
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Total Arrecadado</div>
        <div class="kpi-value" style="color:#60A5FA;">R$ {total_arrecadado:,.2f}</div>
        <div class="kpi-badge-blue">Saldo Atual Real</div>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Total Depósitos</div>
        <div class="kpi-value" style="color:#F8FAFC;">R$ {total_depositos:,.2f}</div>
        <div class="kpi-badge-white">Entradas Brutas</div>
    </div>
    """, unsafe_allow_html=True)
    
with kpi3:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Total Retiradas</div>
        <div class="kpi-value" style="color:#F87171;">R$ {abs(total_retiradas):,.2f}</div>
        <div class="kpi-badge-amber">Saques Realizados</div>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Rendimentos (Juros)</div>
        <div class="kpi-value" style="color:#10B981;">R$ {total_juros:,.2f}</div>
        <div class="kpi-badge-green">Ganhos de Capital</div>
    </div>
    """, unsafe_allow_html=True)

with kpi5:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Falta para Meta</div>
        <div class="kpi-value" style="color:#FBBF24;">R$ {falta_meta:,.2f}</div>
        <div class="kpi-badge-amber">A Arrecadar</div>
    </div>
    """, unsafe_allow_html=True)

with kpi6:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-title">Progresso</div>
        <div class="kpi-value">{pct_meta:.1f}%</div>
        <div style="width: 100%; background-color: #334155; border-radius: 4px; height: 6px; margin-top: 8px;">
            <div style="width: {min(pct_meta, 100)}%; background-color: #3B82F6; height: 100%; border-radius: 4px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# GRÁFICOS
# ==============================================================================
chart_row1_col1, chart_row1_col2 = st.columns(2)
PALETA_CORES = ['#3B82F6', '#10B981', '#8B5CF6', '#F59E0B', '#EC4899', '#06B6D4', '#64748B']

with chart_row1_col1:
    with st.container(border=True):
        # Gráfico 1: Proporção por Pessoa
        fig_pie = px.pie(
            pessoas_only,
            values='Total_Liquido',
            names=col_nome,
            hole=0.55,
            color_discrete_sequence=PALETA_CORES,
            title="<b>1. Contribuição por Pessoa (Líquida, exclui Juros)</b>"
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Total: R$ %{value:,.2f}<br>Participação: %{percent}<extra></extra>",
            hoverlabel=dict(bgcolor="#0F172A", bordercolor="#3B82F6", font=dict(color="white", size=13)),
            marker=dict(line=dict(color='#0F172A', width=3))
        )
        
        if total_arrecadado > 0:
            fig_pie.add_annotation(
                text=f"<span style='font-size:11px;color:#94A3B8'>Total Pessoas</span><br><b style='font-size:16px;color:#F8FAFC'>R$ {pessoas_only['Total_Liquido'].sum():,.2f}</b>",
                x=0.5, y=0.5, showarrow=False
            )
            
        fig_pie.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#F8FAFC", size=12),
            margin=dict(t=45, b=20, l=15, r=15),
            height=330,
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with chart_row1_col2:
    with st.container(border=True):
        # Gráfico 2: Barra Contribuição vs Meta Individual
        pessoas_sorted = pessoas_only.sort_values('Total_Liquido', ascending=True)
        fig_bar = px.bar(
            pessoas_sorted,
            x='Total_Liquido',
            y=col_nome,
            orientation='h',
            title="<b>2. Arrecadado Líquido vs Meta Individual</b>",
            color='Total_Liquido',
            color_continuous_scale=['#1E3A8A', '#2563EB', '#60A5FA'],
            text='Total_Liquido'
        )
        fig_bar.add_vline(x=meta_indiv, line_width=2, line_dash="dash", line_color="#FBBF24",
                         annotation_text=f"Meta: {meta_indiv}", annotation_position="bottom right")
                         
        fig_bar.update_traces(
            texttemplate='R$ %{x:,.2f}',
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Arrecadado: R$ %{x:,.2f}<extra></extra>",
            hoverlabel=dict(bgcolor="#0F172A", bordercolor="#3B82F6", font=dict(color="white", size=13))
        )
        fig_bar.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#F8FAFC", size=12),
            margin=dict(t=45, b=20, l=15, r=60), 
            height=330,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, title="")
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# Linha 2 de Gráficos
if not df_timeline.empty:
    with st.container(border=True):
        # Evolução Temporal de Arrecadação (Soma Cumulativa)
        df_evolucao = df_timeline.sort_values('Data')
        df_evolucao['Valor_Acumulado'] = df_evolucao['Valor'].cumsum()
        
        fig_line = px.area(
            df_evolucao,
            x='Data',
            y='Valor_Acumulado',
            title="<b>3. Evolução da Arrecadação no Tempo</b>",
            color_discrete_sequence=['#10B981']
        )
        fig_line.update_traces(
            hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Saldo Acumulado: R$ %{y:,.2f}<extra></extra>",
            fillcolor='rgba(16, 185, 129, 0.2)',
            line=dict(width=3)
        )
        
        fig_line.add_trace(go.Scatter(
            x=df_evolucao['Data'], 
            y=df_evolucao['Valor_Acumulado'],
            mode='markers',
            marker=dict(size=6, color='#10B981', line=dict(width=1, color='white')),
            name='Movimentações',
            hovertemplate="Data: %{x|%d/%m/%Y}<br>Saldo Total: R$ %{y:,.2f}<extra></extra>"
        ))
        
        fig_line.add_hline(y=meta_total, line_width=2, line_dash="dash", line_color="#FBBF24",
                         annotation_text=f"Meta: {meta_total}", annotation_position="top left")

        fig_line.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#F8FAFC", size=12),
            margin=dict(t=45, b=20, l=15, r=15),
            height=350,
            showlegend=False,
            xaxis=dict(showgrid=True, gridcolor='#1E293B', title=""),
            yaxis=dict(showgrid=True, gridcolor='#1E293B', title="Valor Arrecadado (R$)")
        )
        st.plotly_chart(fig_line, use_container_width=True)

# Tabela Detalhada
st.markdown("---")
st.markdown("### 📋 Tabela de Resumo por Pessoa")
pessoas_disp = pessoas_only[[col_nome, 'Total_Depositos', 'Total_Retiradas', 'Total_Liquido']].copy()
pessoas_disp.columns = ['Participante', 'Total Depósitos (+)', 'Total Retiradas (-)', 'Saldo Líquido (=)']

st.dataframe(pessoas_disp, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### 📅 Histórico de Movimentações")

if not df_timeline.empty:
    disp_timeline = df_timeline[['Data', 'Nome', 'Tipo', 'Valor']].copy()
    disp_timeline = disp_timeline.sort_values(by=['Data', 'Nome'], ascending=[False, True])
    disp_timeline['Data'] = disp_timeline['Data'].dt.strftime('%d/%m/%Y')
    
    st.dataframe(
        disp_timeline,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Data': st.column_config.TextColumn('Data', width='medium'),
            'Nome': st.column_config.TextColumn('Participante', width='medium'),
            'Tipo': st.column_config.TextColumn('Tipo (Depósito/Retirada)', width='medium'),
            'Valor': st.column_config.NumberColumn('Valor (R$)', format='R$ %.2f', width='medium')
        }
    )
else:
    st.info("Nenhuma movimentação encontrada.")
