import streamlit as st
from datetime import datetime
import base64
from PIL import Image
from bs4 import BeautifulSoup
import streamlit.components.v1 as components

# Função para exibir o relatório HTML
def exibir_relatorio():
    follow_up_rows = ''.join(
        [f"<tr><td>{what}</td><td>{who}</td><td>{when.strftime('%d/%m/%Y')}</td><td>{status}</td></tr>" 
         for what, who, when, status in zip(
            st.session_state['follow_up_action_what'], 
            st.session_state['follow_up_action_who'], 
            st.session_state['follow_up_action_when'], 
            st.session_state['follow_up_action_status']
        )]
    )

    def format_text(text):
        return text.replace('\n', '<br>')

    # Process uploaded image for display
    image_html = ""
    if 'uploaded_file' in st.session_state and st.session_state['uploaded_file'] is not None:
        image_bytes = st.session_state['uploaded_file'].read()
        image_b64 = base64.b64encode(image_bytes).decode()
        image_html = f'<img src="data:image/png;base64,{image_b64}" style="max-width: 100%; height: auto;"/>'

    html_content = f"""
    <!doctype html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Relatório</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        <style>
            body, html {{
                width: 100%;
                height: 100%;
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            .container {{
                width: 100%;
                max-width: 100%;
                padding: 10px;
            }}
            .header {{
                background-color: #3A4E5F;
                color: white;
                text-align: center;
                padding: 10px;
                margin-bottom: 5px;
            }}
            .info-line {{
                background-color: #F1F1F1;
                padding: 5px;
                border: 1px solid #D1D1D1;
                margin-bottom: 5px;
            }}
            .info-line strong {{
                margin-right: 15px;
            }}
            .info-container {{
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
            }}
            .info-section {{
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }}
            .section-header {{
                background-color: #3A4E5F;
                color: white;
                padding: 5px;
                margin-top: 5px;
                border-radius: 5px;
            }}
            .subsection-header {{
                background-color: #3A4E5F;
                color: white;
                padding: 5px;
                margin-top: 5px;
                border-radius: 5px;
            }}
            .section-content {{
                border: 1px solid #D1D1D1;
                padding: 5px;
                margin-top: 5px;
                border-radius: 5px;
            }}
            .columns {{
                display: flex;
                flex-wrap: wrap;
            }}
            .column {{
                flex: 1;
                padding: 5px;
                min-width: 300px;
            }}
            .ishikawa {{
                display: flex;
                justify-content: center;
                align-items: center;
                position: relative;
                margin-top: 25px;
                width: 100%;
                min-height: 450px;
                font-size: 9px;
                overflow: hidden;
            }}
            .ishikawa .arrow {{
                position: absolute;
                width: 2px;
                height: 48%;
                background-color: #3A4E5F;
                left: 45%;
                top: 27%;
            }}
            .ishikawa .arrow2 {{
                position: absolute;
                width: 2px;
                height: 57.7%;
                background-color: #3A4E5F;
                left: 15%;
                top: 23%;
            }}
            .ishikawa .arrow3 {{
                position: absolute;
                width: 2px;
                height: 35%;
                background-color: #3A4E5F;
                left: 75%;
                top: 32%;
            }}
            .ishikawa .cabeca {{
                position: absolute;
                width: 0;
                height: 10%;
                border-left: 25px solid #3A4E5F;
                border-top: 45px solid transparent;
                border-bottom: 45px solid transparent;
                left: 95%;
                top: 40%;
            }}
            .ishikawa .line {{
                position: absolute;
                width: 90%;
                height: 2px;
                background-color: #3A4E5F;
                left: 5%;
                top: 50%;
            }}
            .ishikawa .box {{
                position: absolute;
                background-color: white;
                color: black;
                padding: 5px;
                border-radius: 3px;
                text-align: center;
                max-width: 100%; /* Ajuste a largura máxima da caixa para evitar ultrapassar a margem */
                overflow-wrap: break-word; /* Quebra palavras longas */
                height: auto; /* Permite que a altura seja ajustada automaticamente */
                opacity: 0.9;

            }}
            .ishikawa .box input {{
                width: 120px;
                margin-top: 3px;
                display: block;
            }}
            .ishikawa .method {{ top: 20%; left: 15%; transform: translate(-50%, -50%); }}
            .ishikawa .measurement {{ top: 25%; left: 45%; transform: translate(-50%, -50%); }}
            .ishikawa .manpower {{ top: 30%; left: 75%; transform: translate(-50%, -50%); }}
            .ishikawa .environment {{ top: 85%; left: 15%; transform: translate(-50%, -50%); }}
            .ishikawa .material {{ top: 80%; left: 45%; transform: translate(-50%, -50%); }}
            .ishikawa .machine {{ top: 70%; left: 75%; transform: translate(-50%, -50%); }}
            .follow-up-table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 10px;
            }}
            .follow-up-table th, .follow-up-table td {{
                border: 1px solid #D1D1D1;
                padding: 8px;
                text-align: center;
            }}
            .follow-up-table th {{
                background-color: #3A4E5F;
                color: white;
            }}
            @media print {{
                .header, .section-header, .subsection-header {{
                    background-color: #3A4E5F !important;
                    color: white !important;
                }}
                .info-line {{
                    background-color: #F1F1F1 !important;
                }}
                .ishikawa .arrow, .ishikawa .arrow2, .ishikawa .arrow3, .ishikawa .cabeca, .ishikawa .line {{
                    background-color: #3A4E5F !important;
                }}
                .ishikawa .box {{
                    background-color: #3A4E5F !important;
                    color: white !important;
                }}
            }}
            
            .format {{
            background-color: #3A4E5F;
            color: white;
            font-size: 1.2em;
            font-weight: bold;
            padding: 5px;
        }}
            
        </style>

    </head>
    <body>
    <div class="container">
        <div class="header">
            <h1>Relatório A3</h1>
        </div>
        <div class="info-line">
            <div class="info-container">
                <div class="info-section">
                    <strong>Obra:</strong> <span id="obra">{st.session_state['obra']}</span>
                </div>
                <div class="info-section">
                    <strong>Autor:</strong> <span id="autor">{st.session_state['autor']}</span>
                </div>
            </div>
            <div class="info-container">
                <div class="info-section">
                    <strong>Título/Tema:</strong> <span id="titulo">{st.session_state['titulo']}</span>
                </div>
                <div class="info-section">
                    <strong>Data:</strong> <span id="data">{st.session_state['data'].strftime('%d/%m/%Y')}</span>
                </div>
            </div>
        </div>

        <div class="columns">
            <div class="column">
                <div>
                    <div class="section-header">1. Contexto</div>
                    <div class="section-content" id="contexto">{format_text(st.session_state['contexto'])}</div>
                </div>
                <div>
                    <div class="section-header">2. Condições Atuais</div>
                    <div class="section-content" id="condicoes_atuais">
                        {format_text(st.session_state['condicoes_atuais'])}
                        {image_html}
                    </div>
                </div>
                <div>
                    <div class="section-header">3. Meta e objetivos</div>
                    <div class="section-content" id="meta_objetivos">{format_text(st.session_state['meta_objetivos'])}</div>
                </div>
                <div>
                    <div class="section-header">4. Identificação da causa raiz</div>
                    <div class="section-content">
                        <div class="ishikawa">
                            <div class="arrow"></div>
                            <div class="arrow2"></div>
                            <div class="arrow3"></div>
                            <div class="cabeca"></div>
                            <div class="line"></div>
                            <div class="box method">
                                <div class = "format">Método</div>
                                <div id="metodo">{format_text(st.session_state['metodo'])}</div>
                            </div>
                            <div class="box measurement">
                                <div class = "format">Medida</div>
                                <div id="medida">{format_text(st.session_state['medida'])}</div>
                            </div>
                            <div class="box manpower">
                                <div class = "format">Mão de Obra</div>
                                <div id="mao_de_obra">{format_text(st.session_state['mao_de_obra'])}</div>
                            </div>
                            <div class="box environment">
                                <div class = "format">Meio Ambiente</div>
                                <div id="meio_ambiente">{format_text(st.session_state['meio_ambiente'])}</div>
                            </div>
                            <div class="box material">
                                <div class = "format">Material</div>
                                <div id="material">{format_text(st.session_state['material'])}</div>
                            </div>
                            <div class="box machine">
                                <div class = "format">Máquina</div>
                                <div id="maquina">{format_text(st.session_state['maquina'])}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="column">
                <div>
                    <div class="section-header">5. Contramedidas</div>
                    <div class="section-content">
                        <div class="subsection-header">5.1 Contramedidas primordiais para soluções dos problemas</div>
                        <div class="section-content" id="contramedidas_primordiais">{format_text(st.session_state['contramedidas_primordiais'])}</div>
                        <div class="subsection-header">5.2 Contramedidas secundárias para soluções dos problemas</div>
                        <div class="section-content" id="contramedidas_secundarias">{format_text(st.session_state['contramedidas_secundarias'])}</div>
                    </div>
                </div>
                <div>
                    <div class="section-header">6. Condição alvo</div>
                    <div class="section-content" id="condicao_alvo">{format_text(st.session_state['condicao_alvo'])}</div>
                </div>
                <div>
                    <div class="section-header">7. Ações de follow-up para Item 9 - Contramedidas</div>
                    <div class="section-content">
                        <table class="follow-up-table">
                            <thead>
                                <tr>
                                    <th>O que? (What?)</th>
                                    <th>Quem? (Who?)</th>
                                    <th>Quando? (When?)</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody id="follow-up-actions">
                                {follow_up_rows}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    </body>
    </html>
    """
    return html_content

# Função para gerar o link de download do HTML
def gerar_html_download_link(html_content):
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="relatorio.html">Download HTML</a>'
    st.markdown(href, unsafe_allow_html=True)

# Função para limpar os dados do relatório
def limpar_dados_sidebar():
    st.session_state['obra'] = ''
    st.session_state['autor'] = ''
    st.session_state['titulo'] = ''
    st.session_state['data'] = datetime.now()
    st.session_state['contexto'] = ''
    st.session_state['condicoes_atuais'] = ''
    st.session_state['meta_objetivos'] = ''
    st.session_state['metodo'] = ''
    st.session_state['medida'] = ''
    st.session_state['mao_de_obra'] = ''
    st.session_state['meio_ambiente'] = ''
    st.session_state['material'] = ''
    st.session_state['maquina'] = ''
    st.session_state['contramedidas_primordiais'] = ''
    st.session_state['contramedidas_secundarias'] = ''
    st.session_state['condicao_alvo'] = ''
    st.session_state['follow_up_actions'] = []
    st.session_state['uploaded_file'] = None

# Função para carregar os dados do HTML
def carregar_dados_html(uploaded_html):
    soup = BeautifulSoup(uploaded_html, 'html.parser')
    
    st.session_state['obra'] = soup.find(id="obra").text
    st.session_state['autor'] = soup.find(id="autor").text
    st.session_state['titulo'] = soup.find(id="titulo").text
    st.session_state['data'] = datetime.strptime(soup.find(id="data").text, '%d/%m/%Y')
    st.session_state['contexto'] = soup.find(id="contexto").text.replace('<br>', '\n')
    st.session_state['condicoes_atuais'] = soup.find(id="condicoes_atuais").text.replace('<br>', '\n')
    st.session_state['meta_objetivos'] = soup.find(id="meta_objetivos").text.replace('<br>', '\n')
    st.session_state['metodo'] = soup.find(id="metodo").text.replace('<br>', '\n')
    st.session_state['medida'] = soup.find(id="medida").text.replace('<br>', '\n')
    st.session_state['mao_de_obra'] = soup.find(id="mao_de_obra").text.replace('<br>', '\n')
    st.session_state['meio_ambiente'] = soup.find(id="meio_ambiente").text.replace('<br>', '\n')
    st.session_state['material'] = soup.find(id="material").text.replace('<br>', '\n')
    st.session_state['maquina'] = soup.find(id="maquina").text.replace('<br>', '\n')
    st.session_state['contramedidas_primordiais'] = soup.find(id="contramedidas_primordiais").text.replace('<br>', '\n')
    st.session_state['contramedidas_secundarias'] = soup.find(id="contramedidas_secundarias").text.replace('<br>', '\n')
    st.session_state['condicao_alvo'] = soup.find(id="condicao_alvo").text.replace('<br>', '\n')

    st.session_state['follow_up_actions'] = []
    follow_up_rows = soup.find(id="follow-up-actions").find_all('tr')
    for row in follow_up_rows:
        cols = row.find_all('td')
        st.session_state['follow_up_actions'].append({
            'what': cols[0].text,
            'who': cols[1].text,
            'when': datetime.strptime(cols[2].text, '%d/%m/%Y'),
            'status': cols[3].text
        })

# Função principal do Streamlit
def main():
    st.set_page_config(layout="wide")  # Define o layout como wide para ocupar toda a largura da página

    # Custom CSS to reduce the space above the title
    st.markdown(
        """
        <style>
        .css-18e3th9 {
            padding-top: 1rem;
        }
        .stTextArea textarea {
            height: auto !important;
            min-height: 100px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Gerador de Relatórios A3")

    with st.sidebar:
        logo = Image.open("image.png")
        st.image(logo, use_column_width=True)
        
        st.header("Dados do Relatório")
        uploaded_html = st.file_uploader("Upload do arquivo (html) para edição", type=['html'])
        if uploaded_html:
            carregar_dados_html(uploaded_html.getvalue().decode('utf-8'))
        
        st.session_state['obra'] = st.text_input("Obra", st.session_state.get('obra', ''))
        st.session_state['autor'] = st.text_input("Autor", st.session_state.get('autor', ''))
        st.session_state['titulo'] = st.text_input("Título/Tema", st.session_state.get('titulo', ''))
        st.session_state['data'] = st.date_input("Data", value=st.session_state.get('data', datetime.now()))
        st.session_state['contexto'] = st.text_area("1 - Contexto", st.session_state.get('contexto', ''))
        st.session_state['condicoes_atuais'] = st.text_area("2 - Condições Atuais", st.session_state.get('condicoes_atuais', ''))
        st.session_state['uploaded_file'] = st.file_uploader("2.1 - Anexo - Condições Atuais", type=['png', 'jpg', 'jpeg'])
        st.session_state['meta_objetivos'] = st.text_area("3 - Meta e Objetivos", st.session_state.get('meta_objetivos', ''))
        "4 - Identificação da causa raiz"
        st.session_state['metodo'] = st.text_area("4.1 - Método", st.session_state.get('metodo', ''))
        st.session_state['medida'] = st.text_area("4.2 - Medida", st.session_state.get('medida', ''))
        st.session_state['mao_de_obra'] = st.text_area("4.3 - Mão de Obra", st.session_state.get('mao_de_obra', ''))
        st.session_state['meio_ambiente'] = st.text_area("4.4 - Meio Ambiente", st.session_state.get('meio_ambiente', ''))
        st.session_state['material'] = st.text_area("4.5 - Material", st.session_state.get('material', ''))
        st.session_state['maquina'] = st.text_area("4.6 - Máquina", st.session_state.get('maquina', ''))
        "5 - Contramedidas"
        st.session_state['contramedidas_primordiais'] = st.text_area("5.1 - Contramedidas Primordiais", st.session_state.get('contramedidas_primordiais', ''))
        st.session_state['contramedidas_secundarias'] = st.text_area("5.2 - Contramedidas Secundárias", st.session_state.get('contramedidas_secundarias', ''))
        st.session_state['condicao_alvo'] = st.text_area("6 - Condição Alvo", st.session_state.get('condicao_alvo', ''))
        "7. Ações de follow-up"
        # Criar campos dinâmicos para ações de follow-up
        if 'follow_up_actions' not in st.session_state:
            st.session_state['follow_up_actions'] = []

        num_actions = st.number_input("Número de Ações de follow-up", min_value=1, step=1, value=max(1, len(st.session_state['follow_up_actions'])))
        if len(st.session_state['follow_up_actions']) < num_actions:
            for i in range(num_actions - len(st.session_state['follow_up_actions'])):
                st.session_state['follow_up_actions'].append({"what": "", "who": "", "when": datetime.now(), "status": ""})

        for i in range(num_actions):
            st.session_state['follow_up_actions'][i]['what'] = st.text_input(f"O que? (What?) {i+1}", st.session_state['follow_up_actions'][i]['what'])
            st.session_state['follow_up_actions'][i]['who'] = st.text_input(f"Quem? (Who?) {i+1}", st.session_state['follow_up_actions'][i]['who'])
            st.session_state['follow_up_actions'][i]['when'] = st.date_input(f"Quando? (When?) {i+1}", st.session_state['follow_up_actions'][i]['when'])
            st.session_state['follow_up_actions'][i]['status'] = st.text_input(f"Status {i+1}", st.session_state['follow_up_actions'][i]['status'])

        # Botão para apagar dados
        if st.button("Apagar Dados"):
            limpar_dados_sidebar()
            st.experimental_rerun()

    if st.button("Gerar Relatório"):
        st.session_state['follow_up_action_what'] = [action['what'] for action in st.session_state['follow_up_actions']]
        st.session_state['follow_up_action_who'] = [action['who'] for action in st.session_state['follow_up_actions']]
        st.session_state['follow_up_action_when'] = [action['when'] for action in st.session_state['follow_up_actions']]
        st.session_state['follow_up_action_status'] = [action['status'] for action in st.session_state['follow_up_actions']]
        html_content = exibir_relatorio()
        components.html(html_content, height=1500, scrolling=True)
        st.session_state['html_content'] = html_content

    if st.button("Exportar para HTML"):
        if 'html_content' in st.session_state:
            gerar_html_download_link(st.session_state['html_content'])
        else:
            st.warning("Por favor, gere o relatório primeiro.")

if __name__ == "__main__":
    main()
