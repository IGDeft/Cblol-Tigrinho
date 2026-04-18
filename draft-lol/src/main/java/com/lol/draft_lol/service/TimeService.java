package com.lol.draft_lol.service;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.lol.draft_lol.client.PythonDraftClient;

import jakarta.annotation.PostConstruct;

@Service
public class TimeService {
  
  @Autowired
  private PythonDraftClient pythonClient;

  private Set<String> times = new HashSet<>();

  @PostConstruct
  public void carregarTimes(){
    List<String> lista = pythonClient.listarTimes();
    this.times = lista.stream().map(this::normalizar).collect(Collectors.toSet());
    
  }

  public boolean existe(String time){
    return times.contains(normalizar(time));
  }

  public String normalizar(String time){
    return time.toUpperCase().replace("'", "").replace(" ", "_");
  }
}
