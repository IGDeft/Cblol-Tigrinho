package com.lol.draft_lol.DTO;

import com.fasterxml.jackson.annotation.JsonProperty;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;

public record DraftStartDto (

  @Schema(example = "MD3", description= "Quantidade de jogos na serie")
  @NotBlank(message = "O formato não pode estar vazio")
  @JsonProperty("formato")
  String formato,

  @Schema(example = "true", description= "Você vai ser First Pick? sim(true) ou não (false) ")
  @JsonProperty("isFirstPick")
  boolean isFirstPick
  
){}
