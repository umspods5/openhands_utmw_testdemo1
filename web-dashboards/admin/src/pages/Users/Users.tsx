import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,

} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridActionsCellItem,
  GridRowParams,
} from '@mui/x-data-grid';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Block as BlockIcon,
  CheckCircle as VerifyIcon,
} from '@mui/icons-material';

interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  phone_number: string;
  user_type: string;
  is_verified: boolean;
  is_active: boolean;
  date_joined: string;
  building?: string;
}

const Users: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading] = useState(false);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<User | null>(null);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    user_type: 'resident',
    building: '',
  });

  // Mock data - replace with API calls
  useEffect(() => {
    const mockUsers: User[] = [
      {
        id: 1,
        username: 'john_doe',
        email: 'john@example.com',
        first_name: 'John',
        last_name: 'Doe',
        phone_number: '+91 9876543210',
        user_type: 'resident',
        is_verified: true,
        is_active: true,
        date_joined: '2024-01-15',
        building: 'Tower A',
      },
      {
        id: 2,
        username: 'jane_smith',
        email: 'jane@example.com',
        first_name: 'Jane',
        last_name: 'Smith',
        phone_number: '+91 9876543211',
        user_type: 'delivery_agent',
        is_verified: true,
        is_active: true,
        date_joined: '2024-02-20',
      },
      {
        id: 3,
        username: 'admin_user',
        email: 'admin@example.com',
        first_name: 'Admin',
        last_name: 'User',
        phone_number: '+91 9876543212',
        user_type: 'admin',
        is_verified: true,
        is_active: true,
        date_joined: '2024-01-01',
      },
    ];
    setUsers(mockUsers);
  }, []);

  const handleAddUser = () => {
    setSelectedUser(null);
    setFormData({
      username: '',
      email: '',
      first_name: '',
      last_name: '',
      phone_number: '',
      user_type: 'resident',
      building: '',
    });
    setDialogOpen(true);
  };

  const handleEditUser = (user: User) => {
    setSelectedUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      first_name: user.first_name,
      last_name: user.last_name,
      phone_number: user.phone_number,
      user_type: user.user_type,
      building: user.building || '',
    });
    setDialogOpen(true);
  };

  const handleDeleteUser = (id: number) => {
    if (window.confirm('Are you sure you want to delete this user?')) {
      setUsers(users.filter(user => user.id !== id));
    }
  };

  const handleToggleActive = (id: number) => {
    setUsers(users.map(user => 
      user.id === id ? { ...user, is_active: !user.is_active } : user
    ));
  };

  const handleVerifyUser = (id: number) => {
    setUsers(users.map(user => 
      user.id === id ? { ...user, is_verified: true } : user
    ));
  };

  const handleSaveUser = () => {
    if (selectedUser) {
      // Update existing user
      setUsers(users.map(user => 
        user.id === selectedUser.id 
          ? { ...user, ...formData }
          : user
      ));
    } else {
      // Add new user
      const newUser: User = {
        id: Math.max(...users.map(u => u.id)) + 1,
        ...formData,
        is_verified: false,
        is_active: true,
        date_joined: new Date().toISOString().split('T')[0],
      };
      setUsers([...users, newUser]);
    }
    setDialogOpen(false);
  };

  const getUserTypeColor = (userType: string) => {
    switch (userType) {
      case 'admin': return 'error';
      case 'delivery_agent': return 'warning';
      case 'resident': return 'primary';
      default: return 'default';
    }
  };

  const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 70 },
    { field: 'username', headerName: 'Username', width: 130 },
    { field: 'first_name', headerName: 'First Name', width: 130 },
    { field: 'last_name', headerName: 'Last Name', width: 130 },
    { field: 'email', headerName: 'Email', width: 200 },
    { field: 'phone_number', headerName: 'Phone', width: 150 },
    {
      field: 'user_type',
      headerName: 'Type',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={getUserTypeColor(params.value) as any}
          size="small"
        />
      ),
    },
    { field: 'building', headerName: 'Building', width: 100 },
    {
      field: 'is_verified',
      headerName: 'Verified',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Yes' : 'No'}
          color={params.value ? 'success' : 'default'}
          size="small"
        />
      ),
    },
    {
      field: 'is_active',
      headerName: 'Active',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value ? 'Active' : 'Inactive'}
          color={params.value ? 'success' : 'error'}
          size="small"
        />
      ),
    },
    { field: 'date_joined', headerName: 'Joined', width: 120 },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 200,
      getActions: (params: GridRowParams) => [
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => handleEditUser(params.row)}
        />,
        <GridActionsCellItem
          icon={<BlockIcon />}
          label={params.row.is_active ? 'Deactivate' : 'Activate'}
          onClick={() => handleToggleActive(params.row.id)}
        />,
        <GridActionsCellItem
          icon={<VerifyIcon />}
          label="Verify"
          onClick={() => handleVerifyUser(params.row.id)}
          disabled={params.row.is_verified}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Delete"
          onClick={() => handleDeleteUser(params.row.id)}
        />,
      ],
    },
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">User Management</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={handleAddUser}
        >
          Add User
        </Button>
      </Box>

      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={users}
          columns={columns}
          loading={loading}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 10 },
            },
          }}
          checkboxSelection
          disableRowSelectionOnClick
        />
      </Paper>

      {/* Add/Edit User Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {selectedUser ? 'Edit User' : 'Add New User'}
        </DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 1 }}>
            <TextField
              fullWidth
              label="Username"
              value={formData.username}
              onChange={(e) => setFormData({ ...formData, username: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="First Name"
              value={formData.first_name}
              onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Last Name"
              value={formData.last_name}
              onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Phone Number"
              value={formData.phone_number}
              onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
              margin="normal"
            />
            <FormControl fullWidth margin="normal">
              <InputLabel>User Type</InputLabel>
              <Select
                value={formData.user_type}
                onChange={(e) => setFormData({ ...formData, user_type: e.target.value })}
                label="User Type"
              >
                <MenuItem value="resident">Resident</MenuItem>
                <MenuItem value="delivery_agent">Delivery Agent</MenuItem>
                <MenuItem value="admin">Admin</MenuItem>
              </Select>
            </FormControl>
            {formData.user_type === 'resident' && (
              <TextField
                fullWidth
                label="Building"
                value={formData.building}
                onChange={(e) => setFormData({ ...formData, building: e.target.value })}
                margin="normal"
              />
            )}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveUser} variant="contained">
            {selectedUser ? 'Update' : 'Create'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Users;