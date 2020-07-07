#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool check_circle(int winner, int loser);


int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    // put some prints to check the preferences matrix is correct///////
    // printf("     C1  C2  C3  \n");
    // for (int i = 0; i < candidate_count; i++)
    // {
    //     printf("C%i  ", i + 1);
    //     for (int j = 0; j < candidate_count; j++)
    //     {
    //         printf(" %i  ", preferences[i][j]);
    //     }
    //     printf("\n");
    // }
    /////////////////////////////////////////////////////////////

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int c = 0; c < candidate_count; c++)
    {
        if (strcmp(candidates[c], name) == 0)
        {
            ranks[rank] = c;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i; j < candidate_count; j++)
        {
            if (ranks[j] != ranks[i])
            {
                preferences[ranks[i]][ranks[j]] += 1;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }

            if (preferences[j][i] > preferences[i][j])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // THIS IS A SELECTION SORT ALGO //

    int unsorted_length = pair_count;

    // while unsorted list length != 0
    while (unsorted_length != 0)
    {
        // search for the largest value in the list
        int max_val = 0;
        pair max_pair;
        int max_idx;

        for (int i = pair_count - unsorted_length; i < pair_count; i++)
        {
            int winner = pairs[i].winner;
            int loser = pairs[i].loser;
            int diff = preferences[winner][loser] - preferences[loser][winner];

            if (diff > max_val)
            {
                max_pair = pairs[i];
                max_val = diff;
                max_idx = i;
            }
        }

        // copy the first element of the unsorted part of the array into the place of the max value
        pairs[max_idx] = pairs[pair_count - unsorted_length];

        // then copy the max value into the first unsorted element of the array
        pairs[pair_count - unsorted_length] = max_pair;

        // then update the search to only look at the elements of the unsorted part of the array
        unsorted_length--;
    }
    return;
}

// recursively check to see if a locked pair forms a circle.
bool check_circle(int winner, int loser)
{
    // check if THIS loser has beated the winner...
    if (locked[loser][winner] == true)
    {    
        return true;
    }
    // check if LOSER has beaten any other pairs in LOCKED
    for (int i = 0; i < pair_count; i++)
    {
        if (locked[i][winner] == true)
        {
            return check_circle(i, loser);
        }
    }
    // not a circle
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // for each pair in sorted pairs...
    for (int i = 0; i < pair_count; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;

        // check if an edge creates a cycle...?
        if (check_circle(winner, loser) == true)
        {    
            locked[winner][loser] = false;
        }
        else
        {
            locked[winner][loser] = true;
        }
    }
    return;
}



// Print the winner of the election
void print_winner(void)
{
    int max_score = 0;
    int winners[pair_count];
    int num_winners = 0;
    

    // find the highest score
    for (int i = 0; i < pair_count; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        int score = preferences[winner][loser];
        
        if (locked[winner][loser] == true && score > max_score)
        {
            max_score = score;
            //printf("Max Score is now: %i.\n", max_score);
        }
            
    }
    
    // find all locked pairs that have the max score & store them in an array
    for (int i = 0; i < pair_count; i++)
    {
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        int score = preferences[winner][loser];

        if (locked[winner][loser] == true && score == max_score)
        {
            winners[num_winners] = winner;
            num_winners++;
            //printf("Number of winners: %i.\n", num_winners);
        }
    }

    //if (num_winners == 1)
    //{
    //    printf("%s\n", candidates[winners[0]]);
    //    return;
    //}

    // count the frequency of each of the winners array
    int freq[num_winners];
    for (int i = 0; i < num_winners; i++)
    {
        int count = 1;
        for (int j = i + 1; j < num_winners; j++)
        {
            if (winners[i] == winners[j])
            {    
                count++;
                freq[j] = 0;
            }
        }
        
        if (freq[i] != 0)
        {
            freq[i] = count;
        }
        
    }
    
    // Print all unique elements of the array
    for (int i = 0; i < num_winners; i++)
    {
        if (freq[i] == 1)
        {
            printf("%s\n", candidates[winners[i]]);
        }
    }
    return;
}