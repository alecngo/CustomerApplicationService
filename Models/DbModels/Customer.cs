public class Customer
{
    public int Id { get; set; }
    public string Email { get; set; } = default!;
    public string PhoneNumber { get; set; } = default!;
    public string FirstName { get; set; } = default!;
    public string LastName { get; set; } = default!;
    public int ZipCode { get; set; } = default!;
    public string PasswordHash { get; set; } = default!;  // store the hashed password
}
