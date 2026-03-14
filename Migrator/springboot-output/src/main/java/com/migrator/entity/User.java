```java
@Entity
public class User {

    @Id
    @GeneratedValue(strategy = javax.persistence.GenerationType.IDENTITY)
    private Long id;

    // Add remaining fields and getters/setters as needed
}
```