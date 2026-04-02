package com.lol.draft_lol.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import com.lol.draft_lol.DTO.DraftRequestDto;
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
  public Object testat(){
    return pythonClient.obterStatusHome();
  }

  @PostMapping("/prever")
  public ResponseEntity<Object> prever(@RequestBody @Valid DraftRequestDto request){
    Object resultado = draftService.gerarDraft(request);
    return ResponseEntity.ok(resultado);
  }
}
