package com.lol.draft_lol.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import com.lol.draft_lol.pythonAI.RespostaPython;



@RestController
public class DraftController {
  @Autowired
  private RespostaPython pythonClient;

  @GetMapping("/testar") 
  public String status(){
    return "Funcionou";
  }

  @GetMapping("/python")
  public Object testat(){
    return pythonClient.obterStatusHome();
  }
}
