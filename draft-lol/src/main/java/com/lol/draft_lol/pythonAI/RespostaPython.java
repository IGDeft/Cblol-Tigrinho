package com.lol.draft_lol.pythonAI;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

@FeignClient(name="python-ai", url = "http://localhost:5000")
public interface RespostaPython {
  @GetMapping("/")
  Object obterStatusHome();
}
