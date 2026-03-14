```java
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
public class AppDbContext {

    @Id
    @GeneratedValue(strategy = javax.persistence.GenerationType.IDENTITY)
    private Long id;

    // Add other fields as necessary

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }
}
```