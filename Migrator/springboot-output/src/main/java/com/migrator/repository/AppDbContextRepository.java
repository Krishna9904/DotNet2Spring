
package com.migrator.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.migrator.entity.AppDbContext;

public interface AppDbContextRepository extends JpaRepository<AppDbContext, Long> {

}
