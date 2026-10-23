# Procedência e limites de reprodução

Este repositório reúne materiais de um estudo sobre a integração de saídas antecipadas em redes AdaCon, apresentado no SIAC 2026, na UFRJ.

## Materiais próprios do estudo

- `apresentacao_siac_2026.pptx`: apresentação final usada como fonte dos valores publicados aqui.
- `../results/*.csv`: transcrição das tabelas da apresentação (modelos 2B, 3B e 4B; varredura de camadas; calibração de limiar e método).
- `../scripts/*.py`: ferramentas pequenas para conferir e visualizar as tabelas.
- `../figures/*.svg`: gráficos derivados dos CSVs.

As tabelas **não são novas execuções** nem foram calculadas a partir de checkpoints nesta preparação. As tabelas de calibração e validação são provenientes de etapas diferentes do experimento e não devem ser combinadas como se fossem a mesma medição.

## Código de terceiros

`../baseline/adacon/` é um recorte do código-fonte original do [scale-lab/AdaCon](https://github.com/scale-lab/AdaCon), commit `cb8b871` (7 de abril de 2023), distribuído sob GPL-3.0. Ele é mantido como referência à arquitetura de partida. Seus arquivos preservam nomes, interfaces e comentários originais; não são apresentados como desenvolvimento autoral do projeto de pesquisa.

A versão original contém componentes derivados de Ultralytics/YOLOv3. Veja os créditos do AdaCon e o arquivo `../LICENSE`.

## O que falta para reprodução completa

O diretório de trabalho consultado tinha o código público original do AdaCon e apresentações do SIAC, mas não continha os arquivos da modificação com **early exits**, pesos resultantes, logs ou comandos completos de treino/inferência dos experimentos. Assim, este repositório ainda não permite reproduzir as métricas do modelo adaptado a partir de imagens.

Quando os arquivos do experimento estiverem disponíveis, devem ser acrescentados apenas o código de integração, a configuração do experimento e instruções de execução testadas. Pesos grandes e imagens do COCO devem permanecer fora do Git, com instruções de obtenção.
