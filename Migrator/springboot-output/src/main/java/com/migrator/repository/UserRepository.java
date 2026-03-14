
package com.migrator.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.migrator.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {

}
