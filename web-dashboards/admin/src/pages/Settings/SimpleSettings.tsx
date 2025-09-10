import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
} from '@mui/material';
import { Save, Refresh } from '@mui/icons-material';

const SimpleSettings: React.FC = () => {
  const [settings, setSettings] = useState({
    // General Settings
    systemName: 'Smart Locker System',
    adminEmail: 'admin@smartlocker.com',
    supportPhone: '+91 9876543210',
    maxBookingDuration: '48',
    
    // Notification Settings
    emailNotifications: true,
    smsNotifications: true,
    whatsappNotifications: true,
    pushNotifications: false,
    
    // System Settings
    autoCleanup: true,
    maintenanceMode: false,
    debugMode: false,
    logLevel: 'INFO',
    
    // Payment Settings
    razorpayKeyId: 'rzp_test_xxxxxxxxxx',
    razorpayKeySecret: '••••••••••••••••',
    paymentTimeout: '300',
    
    // WhatsApp Settings
    whatsappApiUrl: 'https://api.whatsapp.com',
    whatsappToken: '••••••••••••••••',
    whatsappWebhook: 'https://yourapp.com/webhook',
  });

  const [saved, setSaved] = useState(false);

  const handleInputChange = (field: string, value: string | boolean) => {
    setSettings(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSave = () => {
    // Here you would typically make an API call to save settings
    console.log('Saving settings:', settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const handleReset = () => {
    // Reset to default values
    console.log('Resetting settings to defaults');
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        System Settings
      </Typography>

      {saved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          Settings saved successfully!
        </Alert>
      )}

      <Box display="flex" flexWrap="wrap" gap={3}>
        {/* General Settings */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            General Settings
          </Typography>
          <Box sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="System Name"
              value={settings.systemName}
              onChange={(e) => handleInputChange('systemName', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Admin Email"
              type="email"
              value={settings.adminEmail}
              onChange={(e) => handleInputChange('adminEmail', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Support Phone"
              value={settings.supportPhone}
              onChange={(e) => handleInputChange('supportPhone', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Max Booking Duration (hours)"
              type="number"
              value={settings.maxBookingDuration}
              onChange={(e) => handleInputChange('maxBookingDuration', e.target.value)}
            />
          </Box>
        </Paper>

        {/* Notification Settings */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            Notification Settings
          </Typography>
          <Box sx={{ mt: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.emailNotifications}
                  onChange={(e) => handleInputChange('emailNotifications', e.target.checked)}
                />
              }
              label="Email Notifications"
              sx={{ mb: 1, display: 'block' }}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.smsNotifications}
                  onChange={(e) => handleInputChange('smsNotifications', e.target.checked)}
                />
              }
              label="SMS Notifications"
              sx={{ mb: 1, display: 'block' }}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.whatsappNotifications}
                  onChange={(e) => handleInputChange('whatsappNotifications', e.target.checked)}
                />
              }
              label="WhatsApp Notifications"
              sx={{ mb: 1, display: 'block' }}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.pushNotifications}
                  onChange={(e) => handleInputChange('pushNotifications', e.target.checked)}
                />
              }
              label="Push Notifications"
              sx={{ mb: 1, display: 'block' }}
            />
          </Box>
        </Paper>

        {/* System Settings */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            System Settings
          </Typography>
          <Box sx={{ mt: 2 }}>
            <FormControlLabel
              control={
                <Switch
                  checked={settings.autoCleanup}
                  onChange={(e) => handleInputChange('autoCleanup', e.target.checked)}
                />
              }
              label="Auto Cleanup Expired Bookings"
              sx={{ mb: 1, display: 'block' }}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.maintenanceMode}
                  onChange={(e) => handleInputChange('maintenanceMode', e.target.checked)}
                />
              }
              label="Maintenance Mode"
              sx={{ mb: 1, display: 'block' }}
            />
            <FormControlLabel
              control={
                <Switch
                  checked={settings.debugMode}
                  onChange={(e) => handleInputChange('debugMode', e.target.checked)}
                />
              }
              label="Debug Mode"
              sx={{ mb: 2, display: 'block' }}
            />
            <TextField
              fullWidth
              label="Log Level"
              value={settings.logLevel}
              onChange={(e) => handleInputChange('logLevel', e.target.value)}
            />
          </Box>
        </Paper>

        {/* Payment Settings */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            Payment Settings
          </Typography>
          <Box sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="Razorpay Key ID"
              value={settings.razorpayKeyId}
              onChange={(e) => handleInputChange('razorpayKeyId', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Razorpay Key Secret"
              type="password"
              value={settings.razorpayKeySecret}
              onChange={(e) => handleInputChange('razorpayKeySecret', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Payment Timeout (seconds)"
              type="number"
              value={settings.paymentTimeout}
              onChange={(e) => handleInputChange('paymentTimeout', e.target.value)}
            />
          </Box>
        </Paper>

        {/* WhatsApp Settings */}
        <Paper sx={{ p: 3, flex: 1, minWidth: 400 }}>
          <Typography variant="h6" gutterBottom>
            WhatsApp Settings
          </Typography>
          <Box sx={{ mt: 2 }}>
            <TextField
              fullWidth
              label="WhatsApp API URL"
              value={settings.whatsappApiUrl}
              onChange={(e) => handleInputChange('whatsappApiUrl', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="WhatsApp Token"
              type="password"
              value={settings.whatsappToken}
              onChange={(e) => handleInputChange('whatsappToken', e.target.value)}
              sx={{ mb: 2 }}
            />
            <TextField
              fullWidth
              label="Webhook URL"
              value={settings.whatsappWebhook}
              onChange={(e) => handleInputChange('whatsappWebhook', e.target.value)}
            />
          </Box>
        </Paper>
      </Box>

      <Divider sx={{ my: 3 }} />

      {/* Action Buttons */}
      <Box display="flex" justifyContent="flex-end" gap={2}>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={handleReset}
        >
          Reset to Defaults
        </Button>
        <Button
          variant="contained"
          startIcon={<Save />}
          onClick={handleSave}
          size="large"
        >
          Save Settings
        </Button>
      </Box>
    </Box>
  );
};

export default SimpleSettings;