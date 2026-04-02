package com.lol.draft_lol.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import com.lol.draft_lol.DTO.DraftRequestDto;

import io.swagger.v3.oas.annotations.parameters.RequestBody;

@FeignClient(name="python-ai", url = "http://localhost:5000")
public interface PythonDraftClient {

  @GetMapping("/")
  Object obterStatusHome();

  @PostMapping("/predict")
  Object preverDraft(@RequestBody DraftRequestDto dados);

}
