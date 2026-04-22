package com.lol.draft_lol.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.lol.draft_lol.DTO.DraftAcaoDto;
import com.lol.draft_lol.DTO.DraftProxJogoDto;
import com.lol.draft_lol.DTO.DraftRequestDto;
import com.lol.draft_lol.DTO.DraftStartDto;
import com.lol.draft_lol.DTO.DraftSugestaoDto;
import com.lol.draft_lol.client.PythonDraftClient;
import com.lol.draft_lol.service.DraftService;

import jakarta.validation.Valid;



@RestController
public class DraftController {
  @Autowired
  private PythonDraftClient pythonClient;
  
  @Autowired
  private DraftService draftService;

  @GetMapping("/Testar") 
  public String status(){
    return "Funcionou";
  }

  @GetMapping("/Python")
  public Object testar(){
    return pythonClient.obterStatusHome();
  }

  @GetMapping("/Ligas")
  public Object ligas(){
    return pythonClient.listarLigas();
  }

  @GetMapping("/Times")
  public Object times(){
    return pythonClient.listarTimes();
  }

  @GetMapping("/draft/Sugestao")
  public Object sugerir(@Valid DraftSugestaoDto request) {
      return pythonClient.pedirSugestao(request.sessionId());
  }
  @PostMapping("/Prever")
  public ResponseEntity<Object> prever(@RequestBody @Valid DraftRequestDto request){
    try{
      Object resultado = draftService.gerarDraft(request);
      return ResponseEntity.ok(resultado);
    } catch(IllegalArgumentException e){
      return ResponseEntity.badRequest().body(e.getMessage());
    }
    
  }

  @PostMapping("/draft/Start")
  public Object draftInicio(@RequestBody @Valid DraftStartDto request){
    Object draftIniciado = draftService.criarDraft(request);
    return ResponseEntity.ok(draftIniciado);
  }

  @PostMapping("/draft/Picks-Bans")
  public Object alterarDraft(@RequestBody @Valid DraftAcaoDto request){
    Object draftAlterado = draftService.alterarDraft(request);
    return ResponseEntity.ok(draftAlterado);
  }

  @PostMapping("/draft/Prox-jogo")
  public Object proxJogo(@RequestBody @Valid DraftProxJogoDto request){
    Object draftProxJogo = draftService.proxJogo(request);
    return ResponseEntity.ok(draftProxJogo);
  }
}
