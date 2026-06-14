# 📊 AutomatedSpreadsheets Dashboard
> Um conjunto de projetos em Python que, ao alterar variáveis, permite exportar planilhas e gráficos de forma quase automática. Além disso, conta com um dashboard em Streamlit que atualiza quase instantaneamente!

🔗 **[Acessar o Dashboard](https://luiusu-dashboard-universidades.streamlit.app/?embed_options=dark_theme)**

## 📋 Sobre
Este projeto automatiza o processamento de dados de compras públicas de universidades federais, gerando planilhas consolidadas, resumos e gráficos de forma quase automática. Os dados processados são exibidos em um dashboard interativo construído com Streamlit.

O pipeline completo vai desde a leitura de arquivos CSV brutos até a visualização dinâmica por mês/ano no navegador.

## ⚙️ Funcionalidades

### 🤖 Automação (`automatedSpreadsheets/`)
- Lê arquivos CSV de compras públicas (encoding Windows-1252)
- Filtra registros de universidades pelo nome do órgão
- Calcula o **Custo Total** (Quantidade × Preço Unitário) por item
- Remove entradas com custo zero e ordena do maior para o menor custo
- Exporta duas planilhas por mês:
  - `universidades_{mes}_{ano}.xlsx` — dados detalhados por item
  - `resumo_universidades_{mes}_{ano}.xlsx` — agrupado por universidade
- Gera um gráfico de barras com o custo anual por mês (em bilhões de BRL)
- Exporta o gráfico como imagem `.png`

### 📈 Dashboard (`Dashboard.py` + `pages/Resumo.py`)
- Seleção dinâmica de **ano** e **mês**
- Tabela com os custos do mês selecionado
- Gráfico de barras interativo com o **custo anual acumulado** (em bilhões de BRL)
- **Página de resumo** com gráfico de rosca mostrando a distribuição de custos por universidade (filtrado para aquelas que superam R$ 11,6 milhões)

## 🚀 Como Executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/AutomatedSpreadsheets_Dashboard.git
cd AutomatedSpreadsheets_Dashboard
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Copie o arquivo de exemplo e preencha com seus caminhos:
```bash
cp .env.example .env
```
```env
PLANILHA_BASE2024_mar_ItemCompra.csv=C:\caminho\para\seu\arquivo.csv
CAMINHO=C:\caminho\para\pasta\de\exportacao
```

### 4. Execute o script de processamento
Abra `automatedSpreadsheets/main.py`, ajuste as variáveis `ano` e `mes` no topo do arquivo e execute:
```bash
python automatedSpreadsheets/main.py
```
As planilhas e o gráfico serão exportados automaticamente para a estrutura de pastas `{ano}/{mes}/`.

### 5. Inicie o Dashboard
```bash
streamlit run Dashboard.py
```

## 📁 Formato Esperado dos Dados
O CSV de entrada deve conter pelo menos as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `Nome Órgão` | Nome do órgão comprador |
| `Quantidade Item` | Quantidade comprada |
| `Valor Item` | Preço unitário do item |

> As colunas `Código UG`, `Nome UG` e `Descrição Complementar Item Compra` são removidas automaticamente durante o processamento.

## 🤝 Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.

## 📄 Licença
Este projeto está licenciado sob a **Licença MIT.** Consulte o arquivo `LICENSE` para mais detalhes.
