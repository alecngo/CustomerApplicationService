public class Application
{
    public int Id { get; set; }
    public DateTime Date { get; set; }
    
    public int CustomerId { get; set; } = default!; // Foreign key reference to the users table
    public Customer Customer { get; set; } = default!; // Navigation property

    public int AnimalId { get; set; }  // Foreign key reference to the animals table
    public Animal Animal { get; set; } = default!;  // Navigation property

    public ApplicationStatus Status { get; set; }
}

// Enum to represent the application status
public enum ApplicationStatus
{
    Pending,
    Approved,
    Rejected,
    // ... other statuses as needed
}
