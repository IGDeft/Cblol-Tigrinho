package com.lol.draft_lol.service;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.lol.draft_lol.DTO.DraftAcaoDto;
import com.lol.draft_lol.DTO.DraftRequestDto;
import com.lol.draft_lol.DTO.DraftStartDto;
import com.lol.draft_lol.client.PythonDraftClient;

@Service
public class DraftService {
  
  @Autowired
  private PythonDraftClient pythonClient;

  private TimeService timeService;

  public Object gerarDraft(DraftRequestDto dados){
    if (!timeService.existe(dados.timeA())) {
            throw new IllegalArgumentException("Time não encontrado: " + dados.timeA());
        }
        if (!timeService.existe(dados.timeB())) {
            throw new IllegalArgumentException("Time não encontrado: " + dados.timeB());
        }
    return pythonClient.preverDraft(dados);
  }

  public Object criarDraft(DraftStartDto dados){
    if(!timeService.existe(dados.timeIA())){
      throw new IllegalArgumentException("Time não encontrado: " + dados.timeIA());
    }
    if(!timeService.existe(dados.timeUsuario())){
      throw new IllegalArgumentException("Time não encontrado: " + dados.timeUsuario());
    }
    return pythonClient.iniciarDraft(dados);
  }

  public Object alterarDraft(DraftAcaoDto dados){
    return pythonClient.alterarDraft(dados);
  }
}
