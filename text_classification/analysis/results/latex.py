import pandas as pd
import os

def generate_latex_std_table(df, filename):
    """
    Gera uma tabela LaTeX formatada para dados de desvio padrão.
    """
    try:
        # Nomes das colunas esperadas no formato _std
        original_cols = {
            "metrics": ['accuracy_std', 'precision_std', 'recall_std', 'f1_score_std'],
            "resources": ['mean_ram_usage_std', 'mean_vram_usage_std'],
            "time": 'mean_response_time_std'
        }
        
        df_latex = df.copy()

        # Aplica a formatação de precisão decimal
        for col in original_cols["metrics"] + original_cols["resources"]:
            if col in df_latex.columns:
                df_latex[col] = df_latex[col].apply(
                    lambda x: f'{x:.4f}' if pd.notna(x) else ''
                )
        
        time_col = original_cols["time"]
        if time_col in df_latex.columns:
            df_latex[time_col] = df_latex[time_col].apply(
                lambda x: f'{x:.6f}' if pd.notna(x) else ''
            )

        # Renomeia as colunas para a versão final
        df_latex.rename(columns={
            'model': 'Model',
            'accuracy_std': 'Accuracy',
            'precision_std': 'Precision',
            'recall_std': 'Recall',
            'f1_score_std': 'F1 Score',
            'mean_ram_usage_std': 'RAM (MB)',
            'mean_vram_usage_std': 'VRAM (MB)',
            'mean_response_time_std': 'Time(s)'
        }, inplace=True)

        # Gera o código da tabela
        column_format = 'l@{\\hspace{.5em}}r@{\\hspace{.5em}}r@{\\hspace{.5em}}r@{\\hspace{.5em}}r@{\\hspace{.5em}}r@{\hspace{.5em}}r@{\\hspace{.5em}}r'
        tabular_string = df_latex.to_latex(index=False, escape=False, column_format=column_format, header=True, na_rep="")

        # Monta o bloco LaTeX final com caption e label
        base_name = os.path.splitext(filename)[0].replace('_std', '').replace('_', ' ')
        caption = f"Desvio Padrão dos Modelos para o Dataset {base_name}"
        label = f"tab:{os.path.splitext(filename)[0]}"

        final_latex = f"""% ----- Tabela de Desvio Padrão para: {filename} -----
\\begin{{flushleft}}
\\captionof{{table}}{{{caption}}}
\\label{{{label}}}
{tabular_string}
\\end{{flushleft}}
% ----- Fim da tabela para: {filename} -----
"""
        return final_latex
    except Exception as e:
        return f"% ERRO ao processar {filename}: {e}\\n"

# Lista de todos os seus arquivos de desvio padrão
files_to_process = [
    "results_std_binary1.csv",
    "results_std_binary2.csv",
    "results_std_binary3.csv",
    "results_std_multiclass1.csv",
    "results_std_multiclass2.csv",
    "results_std_multiclass3.csv",
    "results_std_multilabel1.csv",
    "results_std_multilabel2.csv",
    "results_std_multilabel3.csv",
]

# Nome do arquivo de saída
output_filename = "tabelas_latex.txt"

# Abre o arquivo para escrever a saída
with open(output_filename, 'w', encoding='utf-8') as f:
    print(f"Gerando tabelas e salvando em '{output_filename}'...")
    
    # Loop para processar cada arquivo
    for file in files_to_process:
        try:
            df = pd.read_csv(file)
            latex_code = generate_latex_std_table(df, file)
            f.write(latex_code)
            f.write("\n\n") # Adiciona duas linhas em branco entre as tabelas
        except FileNotFoundError:
            error_message = f"% ERRO: Arquivo não encontrado: {file}\\n\\n"
            f.write(error_message)
            print(error_message.strip())

print("Processo finalizado com sucesso!")