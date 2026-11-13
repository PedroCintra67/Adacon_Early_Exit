# Procedência e limites de reprodução

Este repositório reúne materiais de um estudo sobre a integração de saídas antecipadas em redes AdaCon, apresentado no SIAC 2026, na UFRJ.

## Materiais próprios do estudo

- `apresentacao_siac_2026.pdf`: versão revisada apresentada no SIAC 2026, com 17 páginas. É a fonte principal para a comparação-base 2B/3B/4B, a varredura das camadas 49 a 61, a calibração de critérios e limiares e a validação final de **2B com EE na camada 58**.
- `apresentacao_siac_2026_anterior.pptx`: versão anterior, com 20 slides. Mantida como fonte histórica dos resultados de EE para **3B e 4B** que não são apresentados no PDF revisado. Suas referências à camada 61 como configuração final estão desatualizadas.
- `../results/layer_search.csv`, `../results/gate_calibration.csv` e `../results/threshold_calibration.csv`: transcrições das medições do PDF revisado.
- `../results/model_comparison.csv`: resultado final 2B confirmado pelo PDF revisado e resultados 3B/4B preservados do material anterior.
- `../scripts/*.py`: ferramentas pequenas para conferir e visualizar as tabelas.
- `../figures/*.svg`: gráficos gerados localmente a partir dos CSVs, fora do versionamento.

As tabelas **não são novas execuções** nem foram calculadas a partir de checkpoints nesta preparação. As tabelas de calibração e validação são provenientes de etapas diferentes do experimento e não devem ser combinadas como se fossem a mesma medição.

A apresentação revisada escolhe a camada **58** para o resultado final **2B**, enquanto a camada 61 permanece em `layer_search.csv` como alternativa avaliada. Os valores da varredura foram atualizados conforme a tabela do PDF, incluindo as diferenças em AP e GMAC em relação ao PPTX anterior. Os registros de **3B e 4B** em `model_comparison.csv` permanecem associados à camada 58 por uma correção anterior do repositório, mas **o PDF revisado não confirma a camada usada nesses dois experimentos**. Antes de reutilizá-los como resultados finais, é necessário conferir o material original do experimento.

## Código de terceiros

`../baseline/adacon/` é um recorte do código-fonte original do [scale-lab/AdaCon](https://github.com/scale-lab/AdaCon), commit `cb8b871` (7 de abril de 2023), distribuído sob GPL-3.0. Ele é mantido como referência à arquitetura de partida. Seus arquivos preservam nomes, interfaces e comentários originais; não são apresentados como desenvolvimento autoral do projeto de pesquisa.

A versão original contém componentes derivados de Ultralytics/YOLOv3. Veja os créditos do AdaCon e o arquivo `../LICENSE`.

## O que falta para reprodução completa

O diretório de trabalho consultado tinha o código público original do AdaCon e apresentações do SIAC, mas não continha os arquivos da modificação com **early exits**, pesos resultantes, logs ou comandos completos de treino/inferência dos experimentos. Assim, este repositório ainda não permite reproduzir as métricas do modelo adaptado a partir de imagens.

Quando os arquivos do experimento estiverem disponíveis, devem ser acrescentados apenas o código de integração, a configuração do experimento e instruções de execução testadas. Pesos grandes e imagens do COCO devem permanecer fora do Git, com instruções de obtenção.
