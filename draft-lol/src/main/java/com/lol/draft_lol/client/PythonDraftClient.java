package com.lol.draft_lol.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

@FeignClient(name="python-ai", url = "http://localhost:5000")
public interface PythonDraftClient {
  @GetMapping("/")
  Object obterStatusHome();
}
