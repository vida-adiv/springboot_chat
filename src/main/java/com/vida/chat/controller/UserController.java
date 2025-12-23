package com.vida.chat.controller;


import com.vida.chat.models.User;
import com.vida.chat.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
public class UserController {
    @Autowired
    private UserRepository userRepository;

    @GetMapping(path="/user")
    @ResponseBody
    public List<User> getUser(@RequestParam(value = "name",defaultValue = "")String name){
        return userRepository.findByName(name);
    }

    @PostMapping(path="/user/create")
    @ResponseBody
    public String addUser(@RequestBody User user){
        System.out.println("hey there");
        userRepository.save(user);
        return "saved";
    }
    @GetMapping(path="/users")
    @ResponseBody
    public Iterable<User> getAllUsers() {
        // JpaRepository already provides findAll()
        return userRepository.findAll();
    }

}
