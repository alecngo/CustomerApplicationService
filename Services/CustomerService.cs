using Npgsql;

public class CustomerService
{
    private readonly string? _connectionString;

    public CustomerService(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }

    public void AddCustomer(Customer customer)
    {
        using NpgsqlConnection connection = new NpgsqlConnection(_connectionString);
        connection.Open();

        string query = "INSERT INTO customers (Email, PhoneNumber, FirstName, LastName, PasswordHash) VALUES (@Email, @PhoneNumber, @FirstName, @LastName, @PasswordHash)";
        
        using NpgsqlCommand cmd = new NpgsqlCommand(query, connection);
        cmd.Parameters.AddWithValue("@Email", customer.Email);
        cmd.Parameters.AddWithValue("@PhoneNumber", customer.PhoneNumber);
        cmd.Parameters.AddWithValue("@FirstName", customer.FirstName);
        cmd.Parameters.AddWithValue("@LastName", customer.LastName);
        cmd.Parameters.AddWithValue("@PasswordHash", customer.PasswordHash);
        
        cmd.ExecuteNonQuery();
    }
    
    // ... Other customer-related methods
}
