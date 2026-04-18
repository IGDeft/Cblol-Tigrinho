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
public class ChampionService {

  @Autowired
  private PythonDraftClient pythonClient;

  private Set<String> campeoes = new HashSet<>();

  @PostConstruct
  public void carregarCampeoes(){
    List<String> lista = pythonClient.listarCampeoes();
    this.campeoes = lista.stream().map(this::normalizar).collect(Collectors.toSet());
  }

  public boolean existe(String campeao){
    return this.campeoes.contains(normalizar(campeao));
  }

  public String normalizar(String campeao){
    return campeao.toUpperCase().replace("'", "").replace(" ", "_");
  }
}
