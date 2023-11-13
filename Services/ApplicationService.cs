using Npgsql;

public class ApplicationService
{
    private readonly string? _connectionString;

    public ApplicationService(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }

    public Application GetApplicationById(int id)
    {
        Application? application = null;

        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("SELECT * FROM Applications WHERE Id = @Id", connection))
            {
                cmd.Parameters.AddWithValue("@Id", id);
                using (NpgsqlDataReader reader = cmd.ExecuteReader())
                {
                    if (reader.Read())
                    {
                        application = new Application
                        {
                            Id = reader.GetInt32(reader.GetOrdinal("Id")),
                            Date = reader.GetDateTime(reader.GetOrdinal("Date")),
                            CustomerId = reader.GetInt32(reader.GetOrdinal("Customer")),
                            AnimalId = reader.GetInt32(reader.GetOrdinal("Animal")),
                            Status = (ApplicationStatus) Enum.Parse(typeof(ApplicationStatus), reader.GetString(reader.GetOrdinal("Status")))
                        };
                    }
                    else
                    {
                        throw new InvalidOperationException($"No application found with the provided ID: {id}");
                    }
                }
            }
        }

        return application;
    }

    // Add a new application
    public void AddApplication(Application application)
    {
        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("INSERT INTO Applications (Date, Customer, Animal, Status) VALUES (@Date, @Customer, @Animal, @Status)", connection))
            {
                cmd.Parameters.AddWithValue("@Date", application.Date);
                cmd.Parameters.AddWithValue("@Customer", application.CustomerId);
                cmd.Parameters.AddWithValue("@Animal", application.AnimalId);
                cmd.Parameters.AddWithValue("@Status", application.Status);

                cmd.ExecuteNonQuery();
            }
        }
    }

    // Update the status of an application
    public void UpdateApplicationStatus(int applicationId, string newStatus)
    {
        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("UPDATE Applications SET Status = @Status WHERE Id = @Id", connection))
            {
                cmd.Parameters.AddWithValue("@Id", applicationId);
                cmd.Parameters.AddWithValue("@Status", newStatus);

                cmd.ExecuteNonQuery();
            }
        }
    }

    // Delete an application by its ID
    public void DeleteApplication(int id)
    {
        using (NpgsqlConnection connection = new NpgsqlConnection(_connectionString))
        {
            connection.Open();
            using (NpgsqlCommand cmd = new NpgsqlCommand("DELETE FROM Applications WHERE Id = @Id", connection))
            {
                cmd.Parameters.AddWithValue("@Id", id);
                cmd.ExecuteNonQuery();
            }
        }
    }
}
