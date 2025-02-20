#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import wget
import PyPDF2
import re
import tabula
import spacy
import pandas as pd
import re
import streamlit as st
from pathlib import Path


# In[ ]:


def identifica_data_do(texto_formatado):
    
    texto_cortado = texto_formatado[:2000]

    if("Segunda-feira" in texto_cortado):

        data = " Segunda-feira" + texto_formatado.split("Segunda-feira")[1].split("2025")[0]+"2025"

    else:

        if("Terça-feira" in texto_cortado):

            data = " Terça-feira" + texto_formatado.split("Terça-feira")[1].split("2025")[0]+"2025"

        else:

            if("Quarta-feira" in texto_cortado):

                data = " Quarta-feira" + texto_formatado.split("Quarta-feira")[1].split("2025")[0]+"2025"

            else:

                if("Quinta-feira" in texto_cortado):

                    data = " Quinta-feira" + texto_formatado.split("Quinta-feira")[1].split("2025")[0]+"2025"

                else:

                    if("Sexta-feira" in texto_cortado):
 
                        data = " Sexta-feira" + texto_formatado.split("Sexta-feira")[1].split("2025")[0]+"2025"

    return data


# In[ ]:


def formata_texto(texto_formatado):
    
    texto_formatado = texto_formatado.replace("\n", " ")
    texto_formatado = texto_formatado.replace("  ", " ")
    texto_formatado = texto_formatado.replace(" - ", "")
    texto_formatado = texto_formatado.replace("NOMEAR", "Nomear")
    texto_formatado = texto_formatado.replace("ColetivosC", "Coletivos - C")
    texto_formatado = texto_formatado.replace("Sím-bolo", "Símbolo")
    texto_formatado = texto_formatado.replace("DESIGNAR", "Designar")
    texto_formatado = texto_formatado.replace("con ﬁ ança", "confiança")
    texto_formatado = texto_formatado.replace("ja neiro", "janeiro")
    texto_formatado = texto_formatado.replace("- ", "")
    texto_formatado = texto_formatado.replace("-", "")
    texto_formatado = texto_formatado.replace("º.", "º")
    texto_formatado = texto_formatado.replace("AUTORIZO", "Autorizo")
    texto_formatado = texto_formatado.replace("autorizo", "Autorizo")
    texto_formatado = texto_formatado.replace("ADJUDICO", "Adjudico")
    texto_formatado = texto_formatado.replace("adjudico", "Adjudico")
    texto_formatado = texto_formatado.replace("HOMOLOGO", "Homologo")
    texto_formatado = texto_formatado.replace("homologo", "Homologo")
    texto_formatado = texto_formatado.replace("CONTRATO", "Contrato")
    texto_formatado = texto_formatado.replace("contrato", "Contrato")
    texto_formatado = texto_formatado.replace("PROCESSO", "Processo")
    texto_formatado = texto_formatado.replace("processo", "Processo")
    texto_formatado = texto_formatado.replace("PREGÃO ELETRÔNICO", "Pregão Eletrônico")
    texto_formatado = texto_formatado.replace("pregão eletrônico", "Pregão Eletrônico")
    texto_formatado = texto_formatado.replace("Pregão eletrônico", "Pregão Eletrônico")
    texto_formatado = texto_formatado.replace("Prestação de serviços", "Prestação de Serviços")
    texto_formatado = texto_formatado.replace("prestação de serviços", "Prestação de Serviços")
    texto_formatado = texto_formatado.replace("PRESTAÇÃO DE SERVIÇOS", "Prestação de Serviços")
    texto_formatado = texto_formatado.replace("TERMO ADITIVO", "Termo Aditivo")
    texto_formatado = texto_formatado.replace("termo aditivo", "Termo Aditivo")
    texto_formatado = texto_formatado.replace("TERMO DE COLABORAÇÃO", "Termo de Colaboração")
    texto_formatado = texto_formatado.replace("termo de colaboração", "Termo de Colaboração")
    texto_formatado = texto_formatado.replace("licitação", "Licitação")
    texto_formatado = texto_formatado.replace("resultado", "Resultado")
    texto_formatado = texto_formatado.replace("RESULTADO", "Resultado")
    texto_formatado = texto_formatado.replace("AQUISIÇÃO", "Aquisição")
    texto_formatado = texto_formatado.replace("aquisição", "Aquisição")
    texto_formatado = texto_formatado.replace("CONTRATAÇÃO", "Contratação")
    texto_formatado = texto_formatado.replace("contratação", "Contratação")
    texto_formatado = texto_formatado.replace("FORMALIZAÇÃO", "Formalização")
    texto_formatado = texto_formatado.replace("formalização", "Formalização")
    texto_formatado = texto_formatado.replace("R $", "R$")
    texto_formatado = texto_formatado.replace("INEXIGIBILIDADE", "Inexigibilidade")
    texto_formatado = texto_formatado.replace("inexigibilidade", "Inexigibilidade")
    texto_formatado = texto_formatado.replace("Q u", "Qu")
    texto_formatado = texto_formatado.replace("Segundafeira", "Segunda-feira")
    texto_formatado = texto_formatado.replace("Terçafeira", "Terça-feira")
    texto_formatado = texto_formatado.replace("Quartafeira", "Quarta-feira")
    texto_formatado = texto_formatado.replace("Quintafeira", "Quinta-feira")
    texto_formatado = texto_formatado.replace("Sextafeira", "Sexta-feira")
    
    return texto_formatado


# In[ ]:


def identifica_nomes(nomear_designar, subtexto_paragrafo):
    
    nome = ""
    
    if(nomear_designar == "Nomear"):
        
        if("com validade a partir de" in subtexto_paragrafo[:30]):

            if("matrícula" in subtexto_paragrafo.split(",")[2]):

                nome = subtexto_paragrafo.split(",")[1]

            else:

                nome = subtexto_paragrafo.split(",")[2]

        else:

            if("com validade a partir de" in subtexto_paragrafo[15:50]):

                nome = subtexto_paragrafo.split(",")[0]

            else:

                if("com validade de" in subtexto_paragrafo[:30]):

                    nome = subtexto_paragrafo.split(",")[2]

                else:

                    if("com validade a contar de" in subtexto_paragrafo[:30]):

                        nome = subtexto_paragrafo.split(",")[1]

                    else:

                        if(not subtexto_paragrafo.partition(",")[0]):

                            nome = subtexto_paragrafo.partition(",")[2].split(",")[0]

                        else:

                            nome = subtexto_paragrafo.partition(",")[0]
                            
    else:
        
        if(nomear_designar == "Designar" and "fiscais do Termo do Contrato" not in subtexto_paragrafo):
        
            if("com validade a partir de" in subtexto_paragrafo[:30]):

                nome = subtexto_paragrafo.split(",")[2]

            else:

                if("com validade a partir de" in subtexto_paragrafo[15:50]):

                    nome = subtexto_paragrafo.split(",")[0]

                else:

                    if("no período de" in subtexto_paragrafo[:30]):

                        nome = subtexto_paragrafo.split(",")[2]

                    else:

                        if("Nome:" in subtexto_paragrafo):

                            nome = subtexto_paragrafo.split("Nome:")[2]
                            
                        else:

                            if(not subtexto_paragrafo.partition(",")[0]):

                                nome = subtexto_paragrafo.partition("Matrícula")[0]

                            else:

                                nome = subtexto_paragrafo.partition(",")[0]
                           
    return nome


# In[ ]:


def identifica_matricula(nomear_designar, subtexto_paragrafo):
    
    matricula = ""
    
    matricula = subtexto_paragrafo.partition("matrícula")[2].split(",")[0]

    matricula = matricula.replace("nº", "")
    matricula = matricula.replace("n.º", "")
    
    return matricula


# In[ ]:


def identifica_codigo(nomear_designar, subtexto_paragrafo):
    
    codigo = ""
    
    codigo = subtexto_paragrafo.partition("código")[2].split(",")[0]
    
    return codigo    


# In[ ]:


def identifica_validade(nomear_designar, subtexto_paragrafo):
    
    validade = ""
    
    if("a partir de" in subtexto_paragrafo):

        validade = subtexto_paragrafo.partition("a partir de")[2].split(",")[0]

    else:

        if("no período de" in subtexto_paragrafo):

            validade = subtexto_paragrafo.partition("no período de")[2].split(",")[0]
    
    return validade


# In[ ]:


def identifica_funcao(nomear_designar, subtexto_paragrafo):
    
    funcao = ""
    
    if("Cargo em Comissão de" in subtexto_paragrafo):    

        funcao = subtexto_paragrafo.partition("Cargo em Comissão de")[2].split(",")[0]

    else:

        if("cargo em comissão de" in subtexto_paragrafo): 

            funcao = subtexto_paragrafo.partition("cargo em comissão de")[2].split(",")[0]

        else:
            
            if("o Cargo de Confiança de" in subtexto_paragrafo):
                
                funcao = subtexto_paragrafo.partition("o Cargo de Confiança de")[2].split(",")[0]
                
            else:
                
                if("Cargo de confiança de" in subtexto_paragrafo): 

                    funcao = subtexto_paragrafo.partition("Cargo de confiança de")[2].split(",")[0]
                    
                else:
                    
                    if("o Cargo de" in subtexto_paragrafo): 

                        funcao = subtexto_paragrafo.partition("o Cargo de")[2].split(",")[0]

                    else:

                        if("Emprego de Confiança de" in subtexto_paragrafo):

                            funcao = subtexto_paragrafo.partition("Emprego de Confiança de")[2].split(",")[0]

                        else:

                            if("Cargo em Comissão" in subtexto_paragrafo):

                                funcao = subtexto_paragrafo.partition("Cargo em Comissão")[2].split(",")[0]

                            else:

                                if("cargo em comissão" in subtexto_paragrafo):

                                    funcao = subtexto_paragrafo.partition("cargo em comissão")[2].split(",")[0]
                                
                                else:

                                    if("a Função de Confiança de" in subtexto_paragrafo):

                                        funcao = subtexto_paragrafo.partition("a Função de Confiança de")[2].split(",")[0]

                                    else:

                                        if("Coordenador" in subtexto_paragrafo):

                                            funcao = "Coordenador" + subtexto_paragrafo.partition("Coordenador")[2].split(",")[0]

                                        else:

                                            if("Gerente" in subtexto_paragrafo):

                                                funcao = "Gerente" + subtexto_paragrafo.partition("Gerente")[2].split(",")[0]

                                            else:

                                                if("o Cargo de" in subtexto_paragrafo):

                                                    funcao = subtexto_paragrafo.partition("o Cargo de")[2].split(",")[0]

                                                else:

                                                    if("Assessor" in subtexto_paragrafo):

                                                        funcao = "Assessor" + subtexto_paragrafo.partition("Assessor")[2].split(",")[0]

                                                    else:

                                                        if("Secretário" in subtexto_paragrafo):

                                                            funcao = "Secretário" + subtexto_paragrafo.partition("Secretário")[2].split(",")[0]

                                                        else:

                                                            if("Subsecretário" in subtexto_paragrafo):

                                                                funcao = "Subsecretário" + subtexto_paragrafo.partition("Subsecretário")[2].split(",")[0]

                                                            else:

                                                                if("Subsecretária" in subtexto_paragrafo):

                                                                    funcao = "Subsecretária" + subtexto_paragrafo.partition("Subsecretária")[2].split(",")[0]

                                                                else:

                                                                    if("Secretária" in subtexto_paragrafo):

                                                                        funcao = "Secretária" + subtexto_paragrafo.partition("Secretária")[2].split(",")[0]

                                                                    else:

                                                                        if("Coordenadora" in subtexto_paragrafo):

                                                                            funcao = "Coordenadora" + subtexto_paragrafo.partition("Coordenadora")[2].split(",")[0]

                                                                        else:

                                                                            if("Subcontrolador" in subtexto_paragrafo):

                                                                                funcao = "Subcontrolador" + subtexto_paragrafo.partition("Subcontrolador")[2].split(",")[0]

                                                                            else:

                                                                                if("Subcontroladora" in subtexto_paragrafo):

                                                                                    funcao = "Subcontroladora" + subtexto_paragrafo.partition("Subcontroladora")[2].split(",")[0]

                                                                                else:

                                                                                    if("Chefe de Gabinete" in subtexto_paragrafo):

                                                                                        funcao = "Chefe de Gabinete" + subtexto_paragrafo.partition("Chefe de Gabinete")[2].split(",")[0]

                                                                                    else:

                                                                                        if("Supervisor" in subtexto_paragrafo):

                                                                                                funcao = "Supervisor" + subtexto_paragrafo.partition("Supervisor")[2].split(",")[0]

                                                                                        else:

                                                                                            if("Supervisora" in subtexto_paragrafo):

                                                                                                funcao = "Supervisora" + subtexto_paragrafo.partition("Supervisora")[2].split(",")[0]

                                                                                            else:

                                                                                                if("Diretor" in subtexto_paragrafo):

                                                                                                    funcao = "Diretor" + subtexto_paragrafo.partition("Diretor")[2].split(",")[0]

                                                                                                else:

                                                                                                    if("Diretora" in subtexto_paragrafo):

                                                                                                        funcao = "Diretora" + subtexto_paragrafo.partition("Diretora")[2].split(",")[0]                                                                                           
                                                                                            

    funcao = funcao.replace("e r", "er")

    if(" IV" in funcao):

        funcao = funcao.partition(" IV")[0] + funcao.partition(" IV")[1]

    else:

        if(" III" in funcao):

            funcao = funcao.partition(" III")[0] + funcao.partition(" III")[1]

        else:

            if(" II" in funcao):

                funcao = funcao.partition(" II")[0] + funcao.partition(" II")[1]

            else:

                if(" I" in funcao):

                    funcao = funcao.partition(" I")[0] + funcao.partition(" I")[1]
    
    return funcao


# In[ ]:


def identifica_orgao1(nomear_designar, subtexto_paragrafo):
    
    orgao1 = ""
    
    if("Subsecretaria" in subtexto_paragrafo):    

        if("Atenção Primária" in subtexto_paragrafo):

            orgao1 = "Subsecretaria de Promoção, Atenção Primária e Vigilância em Saúde"

        else:
            
            if("Integridade" in subtexto_paragrafo):

                orgao1 = "Subsecretaria de Integridade, Transparência e Proteção de Dados"
                
            else:

                orgao1 = "Subsecretaria" + subtexto_paragrafo.partition("Subsecretaria")[2].split(",")[0]

    else:
        
        if("Instituto Municipal" in subtexto_paragrafo):
                            
            orgao1 = "Instituto Municipal" + subtexto_paragrafo.partition("Instituto Municipal")[2].split(", da")[0]

        else:

            if("Subcontroladoria" in subtexto_paragrafo):

                 orgao1 = "Subcontroladoria" + subtexto_paragrafo.partition("Subcontroladoria")[2].split(",")[0]

            else:

                if("Coordenadoria" in subtexto_paragrafo):    

                    if("Educação" in subtexto_paragrafo):    

                        orgao1 = (subtexto_paragrafo.partition("setor")[2].split("Coordenadoria")[0] + " Coordenadoria" + subtexto_paragrafo.partition("Coordenadoria")[2].split(",")[0])

                        if("da" in orgao1):

                            orgao1 = orgao1.split("da")[1]

                    else:

                        orgao1 = "Coordenadoria" + subtexto_paragrafo.partition("Coordenadoria")[2].split(",")[0]

                else:

                    if("da Diretoria de" in subtexto_paragrafo):    

                        orgao1 = "Diretoria de" + subtexto_paragrafo.partition("da Diretoria de")[2].split(",")[0]

                    else:

                        if("da Presidência" in subtexto_paragrafo or "da PRESIDÊNCIA" in subtexto_paragrafo):    

                            orgao1 = "Presidência"

                        else:

                            if("do Arquivo Geral da Cidade do Rio de Janeiro" in subtexto_paragrafo):    

                                orgao1 = "Arquivo Geral da Cidade do Rio de Janeiro"

                            else:

                                if("do Escritório de" in subtexto_paragrafo):    

                                    orgao1 = "Escritório de" + subtexto_paragrafo.partition("do Escritório de")[2].split(",")[0]

                                else:

                                    if("Chefia" in subtexto_paragrafo):    

                                        orgao1 = "Chefia" + subtexto_paragrafo.partition("Chefia")[2].split(",")[0]
                                        
                                    else:

                                        if("da Diretoria" in subtexto_paragrafo):    

                                            orgao1 = "Diretoria" + subtexto_paragrafo.partition("da Diretoria")[2].split(",")[0]
    
    return orgao1


# In[ ]:


def identifica_orgao2(nomear_designar, subtexto_paragrafo, orgao1):
    
    orgao2 = ""
    
    if("Secretaria" in subtexto_paragrafo):
        
        if("Secretaria Municipal" in subtexto_paragrafo):
            
            orgao2 = "Secretaria Municipal" + subtexto_paragrafo.partition("Secretaria Municipal")[2].split(".")[0]
            orgao2 = orgao2.split(",")[0]
            
        else:

            orgao2 = "Secretaria" + subtexto_paragrafo.partition("Secretaria")[2].split(".")[0]
            orgao2 = orgao2.split(",")[0]

        if(orgao2 == "Secretaria"):

            if("Coordenadoria Regional de Educação" in orgao1):

                orgao2 = "Secretaria Municipal de Educação"
                
        if("Integridade," in subtexto_paragrafo):

            orgao2 = "Secretaria Municipal de Integridade, Transparência e Proteção de Dados"

        else:

            if("Ciência," in subtexto_paragrafo):

                orgao2 = "Secretaria Municipal de Ciência, Tecnologia e Inovação"

    else:

        if("da Fundação" in subtexto_paragrafo):
            
            st.text("Fundação")

            orgao2 = "Fundação" + subtexto_paragrafo.partition("da Fundação")[2].split(".")[0]
            
            st.text(orgao2)

        else:

            if("do Instituto" in subtexto_paragrafo):

                orgao2 = "Instituto" + subtexto_paragrafo.partition("do Instituto")[2].split(".")[0]

            else:

                if("do Gabinete" in subtexto_paragrafo):

                    orgao2 = "Gabinete" + subtexto_paragrafo.partition("do Gabinete")[2].split(".")[0]
                    orgao2 = orgao2.split(",")[0]

                else:

                    if("da Companhia" in subtexto_paragrafo):

                        orgao2 = "Companhia" + subtexto_paragrafo.partition("da Companhia")[2].split(".")[0]
                        orgao2 = orgao2.split(",")[0]

                    else:

                        if("Guarda Municipal" in subtexto_paragrafo):

                            orgao2 = "Guarda Municipal do Rio de Janeiro" 
                            
                        else:
                            
                            if("Controladoria" in subtexto_paragrafo):

                                orgao2 = "Controladoria" + subtexto_paragrafo.partition("Controladoria")[2].split(".")[0]
                                orgao2 = orgao2.split(",")[0]                                
                                
                            else:
                                
                                if("Empresa Municipal" in subtexto_paragrafo):
                                    
                                    if("S.A." in subtexto_paragrafo):

                                        orgao2 = "Empresa Municipal" + subtexto_paragrafo.partition("Empresa Municipal")[2].split(".")[0] + ".A."
                                        orgao2 = orgao2.split(",")[0] 
                                        
                                    else:
                                        
                                        orgao2 = "Empresa Municipal" + subtexto_paragrafo.partition("Empresa Municipal")[2].split(".")[0]
                                        
                                    if("RIOURBE" in orgao2):
                                        
                                        orgao2 = orgao2.replace("RIOURBE", " - RIO-URBE")
                                    
                                else:
                                    
                                    if("Empresa de" in subtexto_paragrafo):

                                        orgao2 = "Empresa de" + subtexto_paragrafo.partition("Empresa de")[2].split(".")[0] + ".A."
                                        orgao2 = orgao2.split(",")[0]
                                
    orgao2 = orgao2.replace("d a", "da")
    return orgao2


# In[ ]:


def identifica_simbolo(nomear_designar, subtexto_paragrafo):
    
    sub_texto_identifica_simbolo = subtexto_paragrafo
    
    simbolo = ""
    
    if(nomear_designar == "Designar"):
        
        if("substituir" in subtexto_paragrafo):

            sub_texto_identifica_simbolo = subtexto_paragrafo.split("substituir")[1]
    
    if("símbolo" in sub_texto_identifica_simbolo):

        simbolo = sub_texto_identifica_simbolo.partition("símbolo")[2].split(",")[0]

    else:

        if("Símbolo" in sub_texto_identifica_simbolo):

            simbolo = sub_texto_identifica_simbolo.partition("Símbolo")[2].split(",")[0]

        else:

            if("DAS" in sub_texto_identifica_simbolo):

                simbolo = "DAS" + sub_texto_identifica_simbolo.partition("DAS")[2].split(",")[0]   
                
    return simbolo  


# In[ ]:


def identifica_nomeacoes(texto_formatado):
    
    nomeacoes = pd.DataFrame()

    cont = 0
    cont_desig = 0
    linha = 0
    nomear_designar = ""

    for palavra in texto_formatado.split():    

        nomear_designar = ""

        if("Nomear" in palavra or "Designar" in palavra):

            if("Nomear" in palavra):

                nomear_designar = "Nomear"
                sub_texto = texto_formatado.split("Nomear")[cont+1]
                cont += 1

            else:

                nomear_designar = "Designar"
                sub_texto = texto_formatado.split("Designar")[cont_desig+1]
                cont_desig += 1

            subtexto_paragrafo = sub_texto[:450]
            subtexto_paragrafo = subtexto_paragrafo.split(". ")[0]

            if("..." not in subtexto_paragrafo):

                if("DAS" in subtexto_paragrafo or "S/E" in subtexto_paragrafo or "Diretor" in subtexto_paragrafo or "Diretora" in subtexto_paragrafo):

                    # NOME

                    nome = identifica_nomes(nomear_designar, subtexto_paragrafo)

                    nomeacoes.at[linha, 'Nome'] = nome

                    # MATRÍCULA e CÓDIGO

                    matricula = ""
                    codigo = ""

                    if(nomear_designar == "Nomear"):

                        if("matrícula" in subtexto_paragrafo):

                            matricula = identifica_matricula(nomear_designar, subtexto_paragrafo)

                        if("código" in subtexto_paragrafo):

                            codigo = identifica_codigo(nomear_designar, subtexto_paragrafo)

                    nomeacoes.at[linha, 'Matrícula'] = matricula
                    nomeacoes.at[linha, 'Código'] = codigo

                    # VALIDADE

                    validade = ""

                    validade = identifica_validade(nomear_designar, subtexto_paragrafo)

                    nomeacoes.at[linha, 'Validade'] = validade

                    # FUNÇÃO              

                    funcao = ""

                    funcao = identifica_funcao(nomear_designar, subtexto_paragrafo)

                    nomeacoes.at[linha, 'Função'] = funcao

                    # SÍMBOLO

                    simbolo = ""

                    simbolo = identifica_simbolo(nomear_designar, subtexto_paragrafo)

                    nomeacoes.at[linha, 'Símbolo'] = simbolo

                    #ÓRGÃO 1

                    orgao1 = ""

                    orgao1 = identifica_orgao1(nomear_designar, subtexto_paragrafo)

                    nomeacoes.at[linha, 'Órgão 1'] = orgao1

                    # ÓRGÃO 2
                    orgao2 = ""

                    orgao2 = identifica_orgao2(nomear_designar, subtexto_paragrafo, orgao1)    

                    nomeacoes.at[linha, 'Órgão 2'] = orgao2

                linha += 1
                
    return nomeacoes


# In[17]:


def nomeacoes_filtrado(nomeacoes):
    
    nomeacoes_filtrado = pd.DataFrame()

    linha = 0

    for i in nomeacoes.index:

        if("10" in nomeacoes.at[i, "Símbolo"] or "S/E" in nomeacoes.at[i, "Símbolo"] or ("Subsecretário" in nomeacoes.at[i, "Função"] and nomeacoes.at[i, "Símbolo"] == "") or ("Diretor" in nomeacoes.at[i, "Função"] and nomeacoes.at[i, "Símbolo"] == "") or ("Diretora" in nomeacoes.at[i, "Função"] and nomeacoes.at[i, "Símbolo"] == "") or ("Secretário" in nomeacoes.at[i, "Função"] and nomeacoes.at[i, "Símbolo"] == "") or "Prefeito" in nomeacoes.at[i, "Função"] or "Subsecretária" in nomeacoes.at[i, "Função"] or "Secretária" in nomeacoes.at[i, "Função"] or "Prefeita" in nomeacoes.at[i, "Função"]):

            nomeacoes_filtrado.at[linha, "Nome"] = nomeacoes.at[i, "Nome"]
            nomeacoes_filtrado.at[linha, "Matrícula"] = nomeacoes.at[i, "Matrícula"]
            nomeacoes_filtrado.at[linha, "Código"] = nomeacoes.at[i, "Código"]
            nomeacoes_filtrado.at[linha, "Validade"] = nomeacoes.at[i, "Validade"]
            nomeacoes_filtrado.at[linha, "Função"] = nomeacoes.at[i, "Função"]
            nomeacoes_filtrado.at[linha, "Símbolo"] = nomeacoes.at[i, "Símbolo"]
            nomeacoes_filtrado.at[linha, "Órgão 1"] = nomeacoes.at[i, "Órgão 1"]
            nomeacoes_filtrado.at[linha, "Órgão 2"] = nomeacoes.at[i, "Órgão 2"]

            linha += 1
            
    return nomeacoes_filtrado


# In[ ]:


def transforma_nomeacoes_texto(nomeacoes_filtrado):
    
    texto = "**Nomeações relevantes:**"
    texto = texto + "\n" + "\n"
    
    for k in nomeacoes_filtrado.index:

        if(nomeacoes_filtrado.at[k, "Nome"] != ""):

            nome = str(nomeacoes_filtrado.at[k, "Nome"]).title()        
            nome = re.sub(r"\b" + "E" + r"\b", "e", nome)
            nome = re.sub(r"\b" + "Da" + r"\b", "da", nome)
            nome = re.sub(r"\b" + "De" + r"\b", "de", nome)
            nome = re.sub(r"\b" + "Dos" + r"\b", "dos", nome)
            
            nome = nome.replace(" - ", "")
            nome = nome.replace("-", "")
            nome = nome.replace("- ", "")
            nome = nome.replace(" -", "")

            texto = texto + nome 

        if(nomeacoes_filtrado.at[k, "Função"] != ""):

            texto = texto + " - " + str(nomeacoes_filtrado.at[k, "Função"])

        if(nomeacoes_filtrado.at[k, "Órgão 1"] != ""):

            texto = texto + ", " + str(nomeacoes_filtrado.at[k, "Órgão 1"])

        if(str(nomeacoes_filtrado.at[k, "Órgão 2"]) != ""):

            texto = texto + ", " + str(nomeacoes_filtrado.at[k, "Órgão 2"])

        if(str(nomeacoes_filtrado.at[k, "Símbolo"]) != ""):

            texto = texto + " (" + str(nomeacoes_filtrado.at[k, "Símbolo"]).strip() + ")"

        texto = texto + "."
        texto = texto + "\n" + "\n"
        
    for palavra in texto.split(" "):
        
        yield palavra + " "

    return texto


# In[ ]:


def limpa_numero(valor):
    
    valor = valor.replace(" 0", " ")
    valor = valor.replace(" 1", " ")
    valor = valor.replace(" 2", " ")
    valor = valor.replace(" 3", " ")
    valor = valor.replace(" 4", " ")
    valor = valor.replace(" 5", " ")
    valor = valor.replace(" 6", " ")
    valor = valor.replace(" 7", " ")
    valor = valor.replace(" 8", " ")
    valor = valor.replace(" 9", " ")
    
    valor = valor.replace(" ", "")
    
    valor = valor.replace("A", " ")
    valor = valor.replace("B", " ")
    valor = valor.replace("C", " ")
    valor = valor.replace("D", " ")
    valor = valor.replace("E", " ")
    valor = valor.replace("F", " ")
    valor = valor.replace("G", " ")
    valor = valor.replace("H", " ")
    valor = valor.replace("I", " ")
    valor = valor.replace("J", " ")
    valor = valor.replace("k", " ")
    valor = valor.replace("L", " ")
    valor = valor.replace("M", " ")
    valor = valor.replace("N", " ")
    valor = valor.replace("O", " ")
    valor = valor.replace("P", " ")
    valor = valor.replace("Q", " ")
    valor = valor.replace("R", " ")
    valor = valor.replace("S", " ")
    valor = valor.replace("T", " ")
    valor = valor.replace("U", " ")
    valor = valor.replace("V", " ")
    valor = valor.replace("W", " ")
    valor = valor.replace("X", " ")
    valor = valor.replace("Y", " ")
    valor = valor.replace("Z", " ")

    valor = valor.replace("a", " ")
    valor = valor.replace("b", " ")
    valor = valor.replace("c", " ")
    valor = valor.replace("d", " ")
    valor = valor.replace("e", " ")
    valor = valor.replace("f", " ")
    valor = valor.replace("g", " ")
    valor = valor.replace("h", " ")
    valor = valor.replace("i", " ")
    valor = valor.replace("j", " ")
    valor = valor.replace("k", " ")
    valor = valor.replace("l", " ")
    valor = valor.replace("m", " ")
    valor = valor.replace("n", " ")
    valor = valor.replace("o", " ")
    valor = valor.replace("p", " ")
    valor = valor.replace("q", " ")
    valor = valor.replace("r", " ")
    valor = valor.replace("s", " ")
    valor = valor.replace("t", " ")
    valor = valor.replace("u", " ")
    valor = valor.replace("v", " ")
    valor = valor.replace("w", " ")
    valor = valor.replace("x", " ")
    valor = valor.replace("y", " ")
    valor = valor.replace("z", " ")

    valor = valor.replace("/", " ")
    valor = valor.replace("%", " ")
    valor = valor.replace("*", " ")
    valor = valor.replace("@", " ")
    valor = valor.replace("#", " ")
    valor = valor.replace("-", " ")
    valor = valor.replace("(", " ")
    valor = valor.replace(";", " ")
    valor = valor.replace("$", " ")
    valor = valor.replace(")", " ")
    valor = valor.replace("º", " ")
    valor = valor.replace(":", " ")

    valor = valor.split()[0]
    
    return valor


# In[ ]:


def identifica_valor(subtexto_paragrafo):
    
    qtd_valores = 0
    
    simbolo = False
    
    numero = True
    
    #print(subtexto_paragrafo)
    
    if('no valor global de ' in subtexto_paragrafo):
        
        if('no valor global de R$ ' not in subtexto_paragrafo):
        
            qtd_valores = subtexto_paragrafo.count("no valor global de ")
            simbolo = False
        
    else:
        
        qtd_valores = subtexto_paragrafo.count("R$ ")
        
        simbolo = True

    valor = ""
    valor_float = 0
    
    #print(str(qtd_valores))

    if(qtd_valores == 1):
        
        if(simbolo):

            valor = subtexto_paragrafo.partition("R$ ")[2]
            
        else:
            
            valor = subtexto_paragrafo.partition("no valor global de ")[2]
            
        if("SIGILOSO" in valor or "Sigiloso" in valor or "sigiloso" in valor):
                
            numero = False
        
        if(numero):
            valor = limpa_numero(valor)            

            valor = valor.replace(".", "")
            valor = valor.replace(",", ".", 1)

            valor = valor.replace(",", " ", 2)

            #print(valor)

            #valor = valor.split()[0]

            valor_float = float(valor)
            

    else:
        
        if("VALOR TOTAL GLOBAL: R$" in subtexto_paragrafo):

            valor = subtexto_paragrafo.partition("VALOR TOTAL GLOBAL: R$")[2]
            
            if("SIGILOSO" in valor or "Sigiloso" in valor or "sigiloso" in valor):
                
                numero = False
                
            if(numero):
            
                valor = limpa_numero(valor)

                valor = valor.replace(".", "")
                valor = valor.replace(",", ".", 1)

                valor = valor.replace(",", " ", 2)

                #print(valor)

                #valor = valor.split()[0]

                valor_float = float(valor)
            
        else:
            
            if("Valores: R$" in subtexto_paragrafo):
                
                valor = subtexto_paragrafo.partition("Valores: R$")[2]
                
                if("SIGILOSO" in valor or "Sigiloso" in valor or "sigiloso" in valor):
                
                    numero = False
                
                if(numero):
                
                    valor = limpa_numero(valor)

                    valor = valor.replace(".", "")
                    valor = valor.replace(",", ".", 1)

                    valor = valor.replace(",", " ", 2)

                    #print(valor)

                    #valor = valor.split()[0]

                    valor_float = float(valor)
                
            else:
                
                if("Valor total: R$" in subtexto_paragrafo):
                    
                    valor = subtexto_paragrafo.partition("Valor total: R$")[2]
                    
                    if("SIGILOSO" in valor or "Sigiloso" in valor or "sigiloso" in valor):
                
                        numero = False
                
                    if(numero):
                        
                        valor = limpa_numero(valor)

                        valor = valor.replace(".", "")
                        valor = valor.replace(",", ".", 1)

                        valor = valor.replace(",", " ", 2)

                        #print(valor)                    

                        #valor = valor.split()[0]                   

                        valor_float = float(valor)
                    
                else:
                     
                    if("Valor: R$" in subtexto_paragrafo):
                    
                        valor = subtexto_paragrafo.partition("Valor: R$")[2]
                        
                        if("SIGILOSO" in valor or "Sigiloso" in valor or "sigiloso" in valor):
                
                            numero = False
                    
                        if(numero):

                            valor = limpa_numero(valor)

                            valor = valor.replace(".", "")
                            valor = valor.replace(",", ".", 1)

                            valor = valor.replace(",", " ", 2)

                            #print(valor)

                            #valor = valor.split()[0]

                            valor_float = float(valor)
                        
                    else:
                        
                        if("R$ " in subtexto_paragrafo):
                    
                            valor = subtexto_paragrafo.partition("R$ ")[2]
                        
                            if("SIGILOSO" in valor or "Sigiloso" in valor or "sigiloso" in valor):
                
                                numero = False
                    
                            if(numero):

                                valor = limpa_numero(valor)

                                valor = valor.replace(".", "")
                                valor = valor.replace(",", ".", 1)

                                valor = valor.replace(",", " ", 2)

                                valor = valor.split()[0]

                                valor_float = float(valor)
    
    return valor_float


# In[ ]:


def identifica_contratacoes(texto_formatado):
    
    contratacoes = pd.DataFrame()

    cont_autorizo = 0
    cont_adjudico = 0
    cont_objeto = 0
    cont_homologo = 0
    cont_processo = 0
    cont_pregao = 0
    cont_processo_doispontos = 0

    linha = 0

    #print(texto_formatado)

    for palavra in texto_formatado.split(): 


        if("Autorizo" in palavra):

            sub_texto = "Autorizo" + texto_formatado.split("Autorizo")[cont_autorizo+1]

            subtexto_paragrafo = sub_texto[:1200]


            if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                #print("***********")
                #print(subtexto_paragrafo)

                if((("Autorizo a Contratação" in subtexto_paragrafo) or ("Autorizo a Aquisição" in subtexto_paragrafo) or ("Autorizo a Formalização" in subtexto_paragrafo and "Contrato" in subtexto_paragrafo) or("Autorizo a formalização" in subtexto_paragrafo and "Termo Aditivo" in subtexto_paragrafo) or ("Autorizo a abertura de licitação" in subtexto_paragrafo) or ("Autorizo apostilamento" in subtexto_paragrafo and "Contrato" in subtexto_paragrafo)) or ("Autorizo a celebração" in subtexto_paragrafo and "Contrato" in subtexto_paragrafo) or ("Termo Aditivo" in subtexto_paragrafo) or ("Autorizo a Chamada Pública" in subtexto_paragrafo)):

                    valor_contrato = identifica_valor(subtexto_paragrafo)

                    if(valor_contrato > 1000000):

                        print("**********")
                        print(subtexto_paragrafo)

                        print(str(valor_contrato))        

            cont_autorizo += 1

        else:

            if("Adjudico" in palavra):

                sub_texto = "Adjudico" + texto_formatado.split("Adjudico")[cont_adjudico+1]
                subtexto_paragrafo = sub_texto[:1200]

                #print("***********")
                #print(subtexto_paragrafo)

                if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                    if(("Homologo" in subtexto_paragrafo and "o Resultado da Licitação" in subtexto_paragrafo) or ("Homologo" in subtexto_paragrafo and "Contratação" in subtexto_paragrafo)):

                        print("**************")
                        print(subtexto_paragrafo)

                        valor_contrato = identifica_valor(subtexto_paragrafo)

                        #print(valor_contrato)

                        if(valor_contrato > 1000000):

                            print("**********")
                            print(subtexto_paragrafo)

                            print(str(valor_contrato))   

                cont_adjudico += 1

            else:

                if("Objeto:" in palavra):

                    sub_texto = "Objeto:" + texto_formatado.split("Objeto:")[cont_objeto+1]
                    subtexto_paragrafo = sub_texto[:1200]

                    #print("***********")
                    #print(subtexto_paragrafo)

                    if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                        if("Aquisição de" in subtexto_paragrafo):

                            valor_contrato = identifica_valor(subtexto_paragrafo)

                            if(valor_contrato > 1000000):

                                print("**********")
                                print(subtexto_paragrafo)

                                print(str(valor_contrato))   

                    cont_objeto += 1

                else:

                    if("Homologo:" in palavra):

                        sub_texto = "Homologo:" + texto_formatado.split("Homologo:")[cont_homologo+1]
                        subtexto_paragrafo = sub_texto[:1200]

                        #print("***********")
                        #print(subtexto_paragrafo)

                        if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                            if("Resultado da Licitação" in subtexto_paragrafo):

                                valor_contrato = identifica_valor(subtexto_paragrafo)

                                if(valor_contrato > 1000000):

                                    print("**********")
                                    print(subtexto_paragrafo)

                                    print(str(valor_contrato))   

                        cont_homologo += 1

                    else:

                        if("Processo:" in palavra):

                            sub_texto = "Processo:" + texto_formatado.split("Processo:")[cont_processo_doispontos+1]
                            subtexto_paragrafo = sub_texto[:1200]

                            #print("***********")
                            #print(subtexto_paragrafo)

                            if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                                if(("Instrutivo" in subtexto_paragrafo and "Contrato" in subtexto_paragrafo) or ("Instrutivo" in subtexto_paragrafo and "Termo de Colaboração" in subtexto_paragrafo)):

                                    valor_contrato = identifica_valor(subtexto_paragrafo)

                                    if(valor_contrato > 1000000):

                                        print("**********")
                                        print(subtexto_paragrafo)

                                        print(str(valor_contrato))   

                                else:

                                    if(("Contratação" in subtexto_paragrafo) or ("Pregão Eletrônico" in subtexto_paragrafo) or ("Prestação de Serviços" in subtexto_paragrafo) or ("Aquisição" in subtexto_paragrafo) or ("Autorizo" in subtexto_paragrafo and "Pregão Eletrônico" in subtexto_paragrafo) or ("Termo Aditivo" in subtexto_paragrafo) or ("Serviços de" in subtexto_paragrafo and "Valor" in subtexto_paragrafo) or ("Contribuição Patronal" in subtexto_paragrafo)):

                                        valor_contrato = identifica_valor(subtexto_paragrafo)

                                        if(valor_contrato > 1000000):

                                            print("**********")
                                            print(subtexto_paragrafo)

                                            print(str(valor_contrato))  

                            cont_processo_doispontos += 1

                        else:

                            if("Pregão Eletrônico:" in palavra):

                                sub_texto = "Pregão Eletrônico" + texto_formatado.split("Pregão Eletrônico")[cont_pregao+1]
                                subtexto_paragrafo = sub_texto[:1200]

                                #print("***********")
                                #print(subtexto_paragrafo)

                                if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                                    if(("Contratação de" in subtexto_paragrafo)):

                                        valor_contrato = identifica_valor(subtexto_paragrafo)

                                        if(valor_contrato > 1000000):

                                            print("**********")
                                            print(subtexto_paragrafo)

                                            print(str(valor_contrato))  

                                cont_pregao += 1 

                            else:

                                if("Processo" in palavra):

                                    sub_texto = "Processo" + texto_formatado.split("Processo")[cont_processo+1]
                                    subtexto_paragrafo = sub_texto[:1200]

                                    #print("**********")
                                    #print(subtexto_paragrafo)

                                    if("R$ " in subtexto_paragrafo or 'no valor global de' in subtexto_paragrafo):

                                        if(("Instrutivo" in subtexto_paragrafo and "Contrato" in subtexto_paragrafo) or ("Instrutivo" in subtexto_paragrafo and "Termo de Colaboração" in subtexto_paragrafo) or ("Instrutivo" in subtexto_paragrafo and "Aquisição" in subtexto_paragrafo)):

                                            #print("**********")
                                            #print(subtexto_paragrafo)

                                            valor_contrato = identifica_valor(subtexto_paragrafo)

                                            if(valor_contrato > 1000000):

                                                print("**********")
                                                print(subtexto_paragrafo)

                                                print(str(valor_contrato))   

                                        else:

                                            if(("Contratação" in subtexto_paragrafo) or ("Pregão Eletrônico" in subtexto_paragrafo) or ("Prestação de Serviços" in subtexto_paragrafo) or ("Aquisição" in subtexto_paragrafo) or ("Autorizo" in subtexto_paragrafo and "Pregão Eletrônico" in subtexto_paragrafo) or ("Termo Aditivo" in subtexto_paragrafo) or ("Serviços de" in subtexto_paragrafo and "Valor" in subtexto_paragrafo) or ("Contribuição Patronal" in subtexto_paragrafo)):  

                                                valor_contrato = identifica_valor(subtexto_paragrafo)

                                                if(valor_contrato > 1000000):

                                                    print("**********")
                                                    print(subtexto_paragrafo)

                                                    print(str(valor_contrato))   

                                    cont_processo += 1


# In[ ]:


arquivo = st.sidebar.text_area("Inclua o link para o pdf do DO da Prefeitura do Rio de Janeiro")
arquivo_selecionado = st.sidebar.button("Enviar")


# In[ ]:


if(arquivo_selecionado):
    
    #nome_arquivo = Path("./Arquivos/" + arquivo.split('/', 6)[6] + ".pdf")
    nome_arquivo = Path(arquivo.split('/', 6)[6] + ".pdf")
    
    if not nome_arquivo.exists():
        
        nome_arquivo_str = str(nome_arquivo)
        
        wget.download(arquivo, nome_arquivo_str)
        st.sidebar.success("Download realizado com sucesso!")
        
    arquivo_pdf = open(nome_arquivo, 'rb')
        
    pdf = PyPDF2.PdfReader(arquivo_pdf)
    
    st.sidebar.success("Arquivo lido com sucesso!")
    
    texto_formatado = ""

    for i in range(len(pdf.pages)):

        pagina = pdf.pages[i]

        texto_formatado = texto_formatado + ''.join(pagina.extract_text())
        
    texto_formatado = formata_texto(texto_formatado)
    
    nomeacoes = identifica_nomeacoes(texto_formatado)
    nomeacoes_filtrado = nomeacoes_filtrado(nomeacoes)
    texto_nomeacoes = transforma_nomeacoes_texto(nomeacoes_filtrado)
    
    data = identifica_data_do(texto_formatado)
    
    titulo = "Análise do Diário Oficial do Município do Rio de Janeiro"
    
    st.subheader(titulo)
    
    st.markdown(":blue["+data+"]")
    
    st.write_stream(texto_nomeacoes)


# In[ ]:




