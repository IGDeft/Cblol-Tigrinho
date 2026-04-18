package com.lol.draft_lol.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.lol.draft_lol.DTO.DraftAcaoDto;
import com.lol.draft_lol.DTO.DraftRequestDto;
import com.lol.draft_lol.DTO.DraftStartDto;
import com.lol.draft_lol.client.PythonDraftClient;
import com.lol.draft_lol.service.DraftService;

import jakarta.validation.Valid;



@RestController
public class DraftController {
  @Autowired
  private PythonDraftClient pythonClient;
  
  @Autowired
  private DraftService draftService;

  @GetMapping("/testar") 
  public String status(){
    return "Funcionou";
  }

  @GetMapping("/python")
  public Object testar(){
    return pythonClient.obterStatusHome();
  }

  @GetMapping("/ligas")
  public Object ligas(){
    return pythonClient.listarLigas();
  }
  @GetMapping("/times")
  public Object times(){
    return pythonClient.listarTimes();
  }

  @PostMapping("/prever")
  public ResponseEntity<Object> prever(@RequestBody @Valid DraftRequestDto request){
    Object resultado = draftService.gerarDraft(request);
    return ResponseEntity.ok(resultado);
  }

  @PostMapping("/draft/start")
  public Object draftInicio(@RequestBody @Valid DraftStartDto request){
    Object draftIniciado = draftService.criarDraft(request);
    return ResponseEntity.ok(draftIniciado);
  }

  @PostMapping("/draft/agir")
  public Object draftInicio(@RequestBody @Valid DraftAcaoDto request){
    Object draftAlterado = draftService.alterarDraft(request);
    return ResponseEntity.ok(draftAlterado);
  }
}
