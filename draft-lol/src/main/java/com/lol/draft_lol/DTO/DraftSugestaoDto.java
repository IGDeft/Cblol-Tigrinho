package com.lol.draft_lol.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public record DraftSugestaoDto (

  @Schema(example = "8255399b-ef4b-4ec4-8636-fa233d857aa3", description = "uuid da sessão")
  @NotBlank(message = "sessionID não pode estar vazio")
  @JsonProperty("sessionId")  
  String sessionId
  
){}
