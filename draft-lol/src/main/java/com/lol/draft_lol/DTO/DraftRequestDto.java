package com.lol.draft_lol.DTO;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;

public record DraftRequestDto (
  @Schema(example = "LOUD", description = "Nome do primeiro time")
  @NotBlank(message = "O time A nao pode estar vazio")
  String timeA,

  @Schema(example = "FURIA", description = "Nome do segundo time")
  @NotBlank(message = "O time B nao pode estar vazio")
  String timeB,

  @Schema(example = "5", description= "Quantidade de jogos (1, 3 ou 5)")
  @Min(1) @Max(5)
  Integer quantidadeJogos
){}
