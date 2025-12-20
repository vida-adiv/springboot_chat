package com.vida.chat.repository;

import com.vida.chat.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<User,Integer> {
    List<User> findByName(String name);
    Optional<User> findById(int id);
}
