package com.vida.chat.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ChatController {

    @GetMapping("/")
    public String hello(@RequestParam(value = "name",defaultValue = "you")String name){
        return String.format("Hey %s",name);
    }
}
