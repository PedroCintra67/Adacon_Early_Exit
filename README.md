# AdaCon + Early Exit 🚀

**Detecção de objetos com processamento adaptativo e saídas antecipadas.**

Projeto de pesquisa desenvolvido na **UFRJ**, no contexto do **Grupo de Teleinformática e Automação (GTA)**, e apresentado no **SIAC 2026** como *Integração de saídas antecipadas em ramos especializados por contexto para detecção de objetos*.

**Autores da apresentação:** Pedro Cintra Silveira, Miguel Elias M. Campista e Daniel Sadoc Menasche.

**A pergunta que guiou o projeto:** é possível reduzir o processamento da detecção de objetos em imagens mais simples sem abrir mão de grande parte da precisão? Investigamos isso combinando o processamento adaptativo do AdaCon com saídas antecipadas (*early exits*).

## 🧠 Como funciona

O trabalho parte do **AdaCon**, uma arquitetura adaptativa baseada em YOLO. O processamento é organizado em quatro componentes:

1. **Backbone compartilhado:** extrai características da imagem, como bordas, formas e texturas.
2. **Branch Controller:** decide quais ramos especializados devem ser utilizados para a cena.
3. **Ramos especializados:** processam conjuntos de classes agrupadas conforme sua coocorrência em imagens.
4. **Cabeças de detecção:** transformam as características em predições de classes e caixas delimitadoras.

A proposta avaliada incorpora **saídas antecipadas (*early exits*)** em pontos intermediários. A confiança da predição é comparada a um limiar `τ`: se atinge o valor exigido, a imagem pode encerrar o processamento; caso contrário, segue até a saída final. Foram avaliados diferentes critérios para agregar a confiança, como média, média ponderada, mediana e mínimo.

### Configurações comparadas

| Configuração | Ramos | Classes por ramo | Contextos |
|:--|--:|:--|:--|
| **2B** | 2 | 49 e 47 | Ambiente externo / ambiente interno |
| **3B** | 3 | 40, 25 e 47 | Animais e esporte / rua / ambiente interno |
| **4B** | 4 | 40, 25, 23 e 40 | Animais e esporte / rua / sala / cozinha |

Os grupos podem compartilhar classes, por isso suas quantidades não somam necessariamente 80. O recorte do código AdaCon original disponível em `baseline/adacon/` inclui a configuração de **quatro ramos**.

## 🗂️ Dataset: COCO 2017

O estudo usou o **Microsoft COCO 2017**, dataset de detecção de objetos com **80 classes** e imagens reais contendo pessoas, animais, veículos, objetos cotidianos, oclusões e diferentes escalas.

A divisão utilizada no estudo foi:

| Conjunto | Imagens | Utilização |
|:--|--:|:--|
| **Treinamento** | **113.287** | Treinamento da rede |
| **Calibração** | **5.000** | Escolha de camadas, métodos e limiares |
| **Validação** | **5.000** | Comparação final das configurações |

As imagens foram processadas em **416 × 416 pixels**. O conjunto oficial `train2017` contém 118.287 imagens; 5.000 foram reservadas para calibração e 113.287 permaneceram no treinamento. As outras 5.000 são do `val2017` oficial. O arquivo com a seleção exata de imagens de calibração não faz parte deste repositório.

Dataset e anotações: [COCO](https://cocodataset.org/#download).

## 🧪 O que avaliamos

O estudo foi organizado em cinco etapas:

1. Treinar o AdaCon e comparar as arquiteturas de **2, 3 e 4 ramos**.
2. Treinar saídas intermediárias e avaliar as camadas **49, 52, 55, 58 e 61**.
3. Comparar métodos de decisão, incluindo média, média ponderada, mínimo e mediana.
4. Avaliar limiares de confiança `τ` entre **0,00 e 1,00**, em passos de **0,05**.
5. Escolher as melhores configurações e medir qualidade, custo e frequência de saída antecipada.

As métricas utilizadas foram **COCO AP (AP50:95)**, precisão média com limiares IoU de 0,50 a 0,95; **GMAC por imagem**, bilhões de operações de multiplicação e acumulação no caminho executado; **% EE**, porcentagem de imagens que saíram antecipadamente; e **AP preservado**, razão entre o AP com saída e o AP da respectiva base.

## 📊 Resultados e principais achados

### Comparação inicial: precisão e custo do AdaCon

| Modelo | COCO AP | GMAC | AP/GMAC |
|:--|--:|--:|--:|
| **2B** | **0,2546** | 28,039 | **0,009081** |
| 3B | 0,2331 | 27,169 | 0,008578 |
| 4B | 0,2268 | **26,735** | 0,008485 |

A configuração **2B** apresentou a maior precisão entre as bases avaliadas e serviu de referência para aprofundar a análise. Já o **4B** teve o menor custo computacional.

### Em qual camada vale a pena antecipar?

| Camada | COCO AP | GMAC da rota | AP/GMAC |
|--:|--:|--:|--:|
| 49 | 0,0968 | **16,879** | 0,0057 |
| 52 | 0,1061 | 17,765 | 0,0060 |
| 55 | 0,1184 | 18,651 | 0,0063 |
| 58 | 0,1333 | 19,537 | 0,0068 |
| **61** | **0,1504** | 20,423 | **0,0074** |

A **camada 61** apresentou o maior AP e a melhor relação AP/GMAC entre as posições estudadas. As camadas anteriores exigiram menos operações, mas perderam mais qualidade de detecção.

### Como calcular a confiança da saída? (calibração)

| Método | `τ` | COCO AP | GMAC | % EE |
|:--|--:|--:|--:|--:|
| Média | 0,40 | 0,2565 | 27,447 | 11,50% |
| **Média ponderada** | **0,40** | 0,2550 | 27,240 | 14,08% |
| Mediana | 0,35 | 0,2532 | **27,235** | **14,16%** |
| Mínimo | 0,25 | **0,2572** | 27,633 | 9,18% |

A escolha foi **média ponderada com `τ = 0,40`**, preservando **97,24% do AP** na calibração.

### Como o limiar afeta precisão e processamento? (calibração)

Configuração **2B**, média ponderada, camada 61:

| `τ` | COCO AP | GMAC | % EE | AP preservado | AP/GMAC |
|--:|--:|--:|--:|--:|--:|
| 0,20 | 0,2049 | **23,221** | **64,70%** | 78,16% | 0,008826 |
| 0,30 | 0,2385 | 25,822 | 31,88% | 90,96% | 0,009236 |
| 0,35 | 0,2498 | 26,713 | 20,68% | 95,27% | 0,009352 |
| **0,40** | **0,2550** | **27,240** | **14,08%** | **97,24%** | **0,009360** |
| 0,45 | 0,2585 | 27,635 | 9,14% | 98,60% | 0,009355 |
| 0,50 | 0,2601 | 27,830 | 6,70% | 99,19% | 0,009346 |

Quanto menor o limiar, mais imagens encerram o processamento cedo. Isso reduz o custo, mas aumenta o risco de perda de AP. A escolha depende do equilíbrio desejado entre velocidade e precisão.

![Efeito do limiar na calibração](figures/threshold_tradeoff.svg)

### Impacto das saídas antecipadas (validação)

| Modelo | AP AdaCon | AP com EE | AP preservado | GMAC AdaCon | GMAC com EE | Redução | % EE |
|:--|--:|--:|--:|--:|--:|--:|--:|
| **2B** | 0,2546 | **0,2491** | **97,83%** | 28,039 | 27,187 | 3,04% | 14,00% |
| **3B** | 0,2331 | 0,2278 | 97,73% | 27,169 | 25,952 | **4,48%** | 20,94% |
| **4B** | 0,2268 | 0,2217 | 97,74% | 26,735 | **25,610** | 4,21% | 20,94% |

Em todos os modelos, foi utilizada **média ponderada**. O limiar foi **0,40 no 2B** e **0,35 nos modelos 3B e 4B**.

A configuração **2B + saída na camada 61 + média ponderada + `τ = 0,40`** teve o maior AP final. Ela reduziu **0,852 GMAC por imagem (3,04%)**, preservando **97,83% do AP**. O **3B** teve a maior redução relativa de GMAC; o **4B**, o menor GMAC absoluto. Assim, diferentes versões fazem sentido dependendo do objetivo da aplicação.

![AdaCon original e AdaCon com saída antecipada](figures/model_comparison.svg)

**Nota sobre os percentuais:** os valores de AP preservado são os publicados nos slides. Como o AP mostrado está arredondado para quatro casas, recalcular a razão a partir dessa tabela pode produzir diferença de aproximadamente 0,01 ponto percentual.

**Calibração e validação são etapas distintas.** Por isso, os valores do ajuste de limiar (AP 0,2550; GMAC 27,240) diferem dos resultados de validação final para 2B (AP 0,2491; GMAC 27,187).

### Quais imagens encerraram o processamento antes?

No modelo 2B, **700 das 5.000 imagens (14,00%)** encerraram cedo o processamento. Essas imagens tinham, em média, **5,52 objetos e 2,42 classes**, contra **7,55 objetos e 3,01 classes** nas demais.

Algumas classes apareceram mais frequentemente em cenas que saíram cedo: **esquis (45,00%)**, **snowboard (42,86%)** e **zebra (37,65%)**. Isso não significa necessariamente maior precisão: esquis, por exemplo, tiveram **4,67% de AP** no subconjunto antecipado. A taxa de saída e a qualidade da detecção devem ser interpretadas separadamente.

A [apresentação do trabalho](docs/apresentacao_siac_2026.pptx) reúne as medições que deram origem às tabelas e aos gráficos deste repositório.

## 🛠️ Ferramentas e tecnologias

| Ferramenta | Para que foi utilizada |
|:--|:--|
| **Python** | Scripts de análise, conferência de métricas e geração de gráficos |
| **PyTorch** | Framework da implementação do detector AdaCon de referência |
| **AdaCon / YOLO** | Base do modelo de detecção com ramos especializados |
| **COCO 2017** | Imagens e anotações usadas no treinamento e na avaliação |
| **pycocotools** | Cálculo das métricas de avaliação no padrão COCO |
| **CSV e SVG** | Organização dos resultados e visualização das comparações |
| **Git e GitHub** | Versionamento e documentação do projeto |

Os scripts incluídos em `scripts/` funcionam com a **biblioteca padrão do Python**, sem instalar PyTorch ou baixar o COCO. As dependências de visão computacional entram em cena ao executar o detector original.

## ▶️ Como executar e explorar os valores

### 1. Conferir a redução de processamento e o AP preservado

Para consultar as métricas registradas no estudo, use **Python 3.9+**. Não é necessário preparar o dataset ou carregar pesos de redes neurais para esses comandos.

Clone o projeto (o GitHub exige acesso, pois este repositório é privado):

```bash
git clone https://github.com/PedroCintra67/Adacon_Early_Exit.git
cd Adacon_Early_Exit
```

Execute o verificador para encontrar, no terminal, **quanto cada modelo 2B, 3B e 4B economizou em GMAC** e **qual porcentagem de AP foi preservada**:

```bash
python scripts/validate_results.py
```

### 2. Visualizar o efeito das saídas antecipadas

Execute o gerador para comparar **o AP e o GMAC antes e depois das saídas antecipadas** e ver **como o limiar muda a taxa de antecipação e a precisão**:

```bash
python scripts/plot_results.py
```

Os dois gráficos são salvos em `figures/model_comparison.svg` e `figures/threshold_tradeoff.svg`. Eles podem ser abertos no navegador ou visualizados no GitHub.

Para consultar os **valores completos** utilizados nesses comandos, os arquivos em `results/` estão separados por assunto:

- [`model_comparison.csv`](results/model_comparison.csv): AP, GMAC e taxa de antecipação nas versões 2B, 3B e 4B;
- [`layer_search.csv`](results/layer_search.csv): desempenho das camadas candidatas;
- [`gate_calibration.csv`](results/gate_calibration.csv): comparação dos métodos de decisão;
- [`threshold_calibration.csv`](results/threshold_calibration.csv): efeito dos limiares de confiança.

Esses comandos **consultam e verificam as medições já registradas**, em vez de executar novamente o treinamento ou a inferência dos modelos da pesquisa.

### 3. Testar a arquitetura AdaCon original

O código-base está em `baseline/adacon/`. Para uma execução de inferência, é preciso instalar as dependências do projeto original, obter seus pesos e fornecer uma imagem.

```bash
cd baseline/adacon
python -m venv .venv
```

Ative o ambiente antes de instalar os pacotes: no PowerShell, execute `.venv\Scripts\Activate.ps1`; em Linux/macOS, `source .venv/bin/activate`. Em seguida:

```bash
python -m pip install -r requirements.txt
```

Com **Bash, wget e conexão à internet**, baixe os pesos da arquitetura original:

```bash
bash weights/download_adacon_weights.sh
```

Verifique os caminhos dos arquivos no `model.args` e execute a inferência sobre uma imagem local:

```bash
python detect.py --adaptive --model model.args --source caminho/da/imagem.jpg --img-size 416
```

Este exemplo utiliza **AdaCon original de quatro ramos**. As versões e os pesos desse projeto da literatura são legados; essa instalação e a inferência não foram executadas nesta preparação.

Para avaliar o **AdaCon original** sobre o COCO, também existe `test.py` no diretório `baseline/adacon/`. Ele exige as imagens e anotações oficiais, os caminhos configurados em `data/coco2017.data` e os pesos indicados em `model.args`.

O código em `baseline/` corresponde à arquitetura original da literatura, com quatro ramos. A implementação experimental das saídas antecipadas e seus checkpoints não estão neste recorte; os comandos das duas primeiras etapas são o caminho disponível para **encontrar e analisar os resultados da pesquisa**.

## 📁 Organização do repositório

```text
Adacon_Early_Exit/
├── baseline/adacon/    # código original AdaCon e configurações
├── docs/               # apresentação SIAC e procedência
├── figures/            # visualizações dos dados
├── results/            # resultados em CSV
├── scripts/            # validação e gráficos
├── .gitignore
├── LICENSE
└── README.md
```

## 📚 Referências e créditos

- M. Neseem e S. Reda, *AdaCon: Adaptive Context-Aware Object Detection for Resource-Constrained Embedded Devices*, ICCAD 2021. [Artigo](https://arxiv.org/abs/2108.06850) · [Código original](https://github.com/scale-lab/AdaCon).
- S. Teerapittayanon, B. McDanel e H. T. Kung, *BranchyNet: Fast Inference via Early Exiting from Deep Neural Networks*, ICPR 2016.
- T.-Y. Lin et al., *Microsoft COCO: Common Objects in Context*, ECCV 2014.

O recorte do código AdaCon em `baseline/adacon/` mantém sua **licença GPL-3.0** e a atribuição aos autores originais. A [documentação de procedência](docs/PROVENIENCIA.md) detalha a origem dos arquivos.
