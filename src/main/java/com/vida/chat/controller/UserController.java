package com.vida.chat.controller;


import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {

    @GetMapping("/user")
    public String getUser(@RequestParam(value = "name",defaultValue = "")String name){
        if(name.isEmpty()){
            //get all users
            return "all users placeholder";
        }
        else{
            //get user by name
            return "named user placeholder";
        }
    }


}
