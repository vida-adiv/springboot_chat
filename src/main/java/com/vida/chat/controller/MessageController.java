package com.vida.chat.controller;

import com.vida.chat.models.Message;
import com.vida.chat.models.MessageResponse;
import com.vida.chat.repository.MessageRepository;
import org.jspecify.annotations.NonNull;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@Controller
public class MessageController {

    @Autowired
    private MessageRepository messageRepository;


    @PostMapping(path="/msg",
    consumes = MediaType.APPLICATION_JSON_VALUE,
    produces = MediaType.APPLICATION_JSON_VALUE)
    @ResponseBody
    public ResponseEntity<@NonNull MessageResponse> sendMsg(@RequestBody Message msg){
        messageRepository.save(msg);
        return ResponseEntity.accepted().body(new MessageResponse(200, "saved"));
    }

    @GetMapping(path="/msg")
    @ResponseBody
    public List<Message> getMsg(@RequestParam (value="rec") int rec){
        //todo get recipient id from token, otherwise this is NOT SECURE!!!
        return messageRepository.findByRec(rec);
    }

    @DeleteMapping(path="/msg/{id}",
    consumes =MediaType.APPLICATION_JSON_VALUE,
            produces=MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<@NonNull MessageResponse> deleteMsg(@PathVariable int id){
        //TODO verify user
        Optional<Message> optionalMessage = messageRepository.findById(id);
        if (optionalMessage.isPresent()) {
            messageRepository.deleteById(id);
            return ResponseEntity.accepted().body(new MessageResponse(200, "deleted"));
        } else {
            return ResponseEntity.badRequest().body(new MessageResponse(404, "message not found"));
        }
    }
}
