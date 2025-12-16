package com.vida.chat.repository;

import com.vida.chat.models.User;
import org.springframework.data.repository.CrudRepository;

import java.util.List;

public interface UserRepository extends CrudRepository<User,Long> {
    List<User> findByName(String name);
    User findById(long id);
}
