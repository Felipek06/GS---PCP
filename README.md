# Sistema de Carreiras

Ferramenta em Python com interface Tkinter para cadastro de perfis e análise automática de compatibilidade com diferentes carreiras.  
O sistema oferece uma visualização clara e objetiva do alinhamento entre competências individuais e exigências profissionais.

## Funcionalidades
- Cadastro, edição e exclusão de perfis  
- Salvamento automático em arquivo JSON  
- Análise de compatibilidade com quatro carreiras predefinidas  
- Cálculo de compatibilidade média com barra de progresso  
- Interface gráfica intuitiva desenvolvida em Tkinter  

## Estrutura do Sistema
- **Competencia:** representa uma habilidade específica, contendo nome e valor  
- **Perfil:** conjunto de competências pertencentes a um usuário  
- **Carreira:** definição de pesos, requisitos e lógica de compatibilidade para cada profissão  
- **SistemaApp:** módulo responsável pela interface gráfica e fluxo geral da aplicação  

## Como Executar
1. Instale o Python 3 em sua máquina.  
2. Baixe o projeto ou clone o repositório.  
3. Execute o arquivo principal:

   ```bash
   python main.py
