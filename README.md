Exportador de Dados do Firebase
Este projeto é um exportador de dados do Firebase que permite visualizar, filtrar e exportar dados do Firebase em formato CSV. A aplicação é construída com PyQt5 e se conecta ao Firebase para obter e exibir dados básicos em uma tabela interativa.

Funcionalidades
Visualização de Dados: Exibe dados do Firebase em uma tabela com suporte para várias colunas e linhas.
Filtros: Permite aplicar filtros por coluna para refinar os dados exibidos.
Exportação: Exporta os dados filtrados para um arquivo CSV.
Interface Gráfica: Utiliza PyQt5 para uma interface gráfica intuitiva e interativa.
Requisitos
Python: 3.x
PyQt5: Para a interface gráfica.
Pandas: Para manipulação e exportação de dados.
Firebase Admin SDK: Para a integração com o Firebase.
Instalação
Clone o Repositório

bash
Copiar código
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
Crie um Ambiente Virtual (opcional, mas recomendado)

bash
Copiar código
python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`
Instale as Dependências

bash
Copiar código
pip install -r requirements.txt
Configure o Firebase

Obtenha o arquivo de configuração do Firebase firebase-admin.json e coloque-o na raiz do projeto.
Certifique-se de que firebase-admin.json está incluído no .gitignore para proteger informações sensíveis.
Uso
Execute o Aplicativo

bash
Copiar código
python main.py
Navegue pela Interface

Dados Básicos: Visualize e filtre os dados obtidos do Firebase.
Exportar CSV: Clique no botão "Exportar CSV" para salvar os dados filtrados em um arquivo CSV.
Estrutura do Projeto
main.py: Arquivo principal que inicia a aplicação.
firebase_service.py: Serviço de integração com o Firebase.
page_licencas.py: Página para exibir dados de licenças.
page_dados_basicos.py: Página para exibir dados básicos e aplicar filtros.
requirements.txt: Lista de dependências do projeto.
Contribuição
Contribuições são bem-vindas! Se você encontrar um bug ou tiver uma melhoria, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Licença
Este projeto é licenciado sob a Licença MIT.
